from tkinter import messagebox, filedialog, ttk, FLAT, RAISED
import tkinter as tk
from PIL import Image, ImageTk
import socket
import pickle


password_protocol = 'pa'
username_protocol = 'us'
pictures_protocol = 'pi'
password_exist = '1'
password_not_exist = '2'
username_exist = 'a'
username_not_exist = 'b'

NUMBER = 1
LARGEFONT = ("Times New Roman", 35)
MEDIUM1 = ("Impact", 12)
MEDIUM2 = ("Helvetica", 10)
dictionary = {"Home Page": 1, 'Go to Page1 - To Login': 2, '"Log in to see pictures"': 3, "Pictures Page": 4,
              "Edit Pictures Page": 5, "Upload Pictures Page": 6, 'GoodBye - To exit': 7}
Home_Page = "Home Page"
Sign_Up_Page = "To Sign up"
Log_in_Page = "Log in to see pictures"
Pictures_Page = "Pictures Page"
Edit_Pictures_Page = "Edit Pictures Page"
Upload_pictures_Page = "Upload Pictures Page"
exit_button = 'GoodBye - To exit'

storage_user_name = []
storage_password = []
storage_pictures = []
USER_NAME = ''
PASSWORD = ''
count_pictures = 1
count_five_pictures = 0

EDIT_IMAGE = ''
BUTTON_IMAGE = ''
IF_IMAGE_PRESSED = False
NUMBER_PICTURES = 0

panel = None
access = False


def exit_window(button_value):
    global NUMBER, root
    print(button_value)
    print(f"Button pressed: {button_value} with the value: {dictionary[button_value]} ")
    if dictionary[button_value] == 7:
        print("GoodBye")
        root.quit()


def exist_check(entry_user_name):
    for username in storage_user_name:
        if entry_user_name == username:
            return True


def show_text(entry_user_name, entry_password, frame):
    global USER_NAME, PASSWORD
    USER_NAME = entry_user_name.get()
    PASSWORD = entry_password.get()
    if USER_NAME == '' or PASSWORD == '':
        tk.Label(frame, text="Something went wrong please try again", font=MEDIUM1).\
            place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
    elif exist_check(USER_NAME):
        tk.Label(frame, text="This user name is taken", font=MEDIUM1).\
            place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
    else:
        tk.Label(frame, text=f"Your user name is: -> {USER_NAME} <-", font=MEDIUM2). \
            place(x=650, y=300, anchor=tk.CENTER, width=240, height=50)
        print(f"Your username -> {USER_NAME}")
        tk.Label(frame, text=f"Your password is: -> {PASSWORD} <-", font=MEDIUM2). \
            place(x=650, y=400, anchor=tk.CENTER, width=240, height=50)
        print(f"With the password -> {PASSWORD} <-")
        # sends the username and the password to server for storage them in the database
        msg_name = username_protocol, USER_NAME
        s.sendall(pickle.dumps(msg_name))
        msg_password = password_protocol, PASSWORD
        s.sendall(pickle.dumps(msg_password))
        storage_user_name.append(USER_NAME)
        storage_password.append(PASSWORD)

    print(f'The username storage: {storage_user_name}')
    print(f'The password storage: {storage_password}')


def select_image(frame, select_image_button):
    global NUMBER_PICTURES, EDIT_IMAGE
    if EDIT_IMAGE == '':
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                global panel
                image = Image.open(file_path)
                image = image.resize((200, 200), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)
                if panel is None:
                    panel = tk.Label(frame, image=image)
                    panel.image = image
                    # The client sends the picture to the server to his DataBase
                    storage_pictures.append(image)
                    panel.place(x=100+200*NUMBER_PICTURES, y=150, anchor=tk.CENTER)
                    NUMBER_PICTURES += 1
                else:
                    panel.configure(image=image)
                    panel.image = image
                panel = None
                if NUMBER_PICTURES > 4:
                    tk.Label(frame, text="You can upload up to five pictures", font=MEDIUM1). \
                        place(x=500, y=500, anchor=tk.CENTER, width=300, height=50)
                    select_image_button.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", "Failed to open image\n{}".format(e))
    else:
        storage_pictures.append(EDIT_IMAGE)
        tk.Button(frame, text="Are you sure you want to upload this?", font=MEDIUM1)
        frame.master.switch_frame(PicturesPage1)


def reset_pictures(frame):
    global storage_pictures
    storage_pictures = None
    tk.Label(frame, text="All the storage got reset").pack()


def switch_to_pictures(entry_user_name, entry_password, frame):
    # sends the username and the password to the sever for checking them in the database
    global access
    access = False
    print(f'User name: {entry_user_name.get()}, Password: {entry_password.get()}')
    msg_name = username_protocol + 'l', entry_user_name.get()
    s.sendall(pickle.dumps(msg_name))
    access_password = pickle.loads(s.recv(1024))
    msg_password = password_protocol + 'l', entry_password.get()
    s.sendall(pickle.dumps(msg_password))
    access_username = pickle.loads(s.recv(1024))
    if access_password == password_exist and access_username == username_exist:
        access = True
    elif access_password == password_not_exist and access_username == username_not_exist:
        access = False

    print(access)
    if access:
        frame.master.switch_frame(PicturesPage1)
    else:
        tk.Label(frame, text="Your username or password is incorrect", font=MEDIUM1).\
            place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)


def marked_image(image, button_image, frame):
    global EDIT_IMAGE, BUTTON_IMAGE, IF_IMAGE_PRESSED
    tk.Button(frame, text="Resets marked picture", command=lambda: reset_marked_image()).\
        place(x=775, y=660, anchor=tk.CENTER, width=350, height=30)
    if not IF_IMAGE_PRESSED:
        EDIT_IMAGE = image
        BUTTON_IMAGE = button_image
        BUTTON_IMAGE.config(relief=tk.SOLID, bd=4, bg="#FFC107")
        IF_IMAGE_PRESSED = True
    else:
        BUTTON_IMAGE.config(relief=FLAT, bd=4, bg="white")
        BUTTON_IMAGE = button_image
        BUTTON_IMAGE.config(relief=tk.SOLID, bd=4, bg="#FFC107")


def reset_marked_image():
    global BUTTON_IMAGE, EDIT_IMAGE
    EDIT_IMAGE = ''
    BUTTON_IMAGE.config(relief=FLAT, bd=4, bg="white")


def print_pictures(image, frame):
    global panel, count_pictures, count_five_pictures
    if panel is None:
        button_image = tk.Button(frame, image=image, relief=FLAT, bd=4, bg="white",
                                 command=lambda: marked_image(image, button_image, frame))
        panel = button_image
        panel.place(x=110 + (210 * count_pictures),
                    y=200 + (280 * count_five_pictures), anchor=tk.CENTER)
        count_pictures += 1
        if count_pictures / 5 == 1:
            count_five_pictures = (count_pictures / 5)
            count_pictures = 0
    else:
        panel.configure(image=image)
        panel.image = image


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)


class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Start Page - managing and editing photos", font=LARGEFONT).\
            place(x=600, y=50, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text="For the Clients", font=MEDIUM1).\
            place(x=600, y=950, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text=Sign_Up_Page, relief=RAISED,
                  command=lambda: master.switch_frame(SignUpPage)).\
            place(x=200, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text=Log_in_Page, relief=RAISED,
                  command=lambda: master.switch_frame(LogInPage)).\
            place(x=600, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text=exit_button, relief=RAISED,
                  command=lambda: exit_window(exit_button)).\
            place(x=1000, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Label(self, text="For the Host", font=MEDIUM1).\
            place(x=600, y=365, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Reset pictures", relief=RAISED,
                  command=lambda: reset_pictures(self)).\
            place(x=600, y=400, anchor=tk.CENTER, width=400, height=50)


class SignUpPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Sign in section", font=LARGEFONT).\
            place(x=600, y=100, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Please enter User Name: ", font=MEDIUM1).\
            place(x=100, y=300, anchor=tk.CENTER, width=200, height=50)
        entry_user_name = ttk.Entry(self, font="Verdana")
        entry_user_name.\
            place(x=300, y=300, anchor=tk.CENTER, width=200, height=25)
        tk.Label(self, text=f"Please enter PassWord: ", font=MEDIUM1).\
            place(x=100, y=400, anchor=tk.CENTER, width=200, height=50)
        entry_password = ttk.Entry(self, font="Verdana")
        entry_password.\
            place(x=300, y=400, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="Sign Up", relief=RAISED,
                  command=lambda: show_text(entry_user_name, entry_password, self)).\
            place(x=100, y=600, anchor=tk.CENTER, width=200, height=50)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)).\
            place(x=300, y=600, anchor=tk.CENTER, width=200, height=50)


class LogInPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text=Log_in_Page, font=LARGEFONT).\
            place(x=600, y=100, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Please enter User Name:").\
            place(x=100, y=300, anchor=tk.CENTER, width=200, height=50)
        entry_user_name = ttk.Entry(self, font="Verdana")
        entry_user_name.\
            place(x=300, y=300, anchor=tk.CENTER, width=200, height=25)
        tk.Label(self, text=f"Please enter Password").\
            place(x=100, y=400, anchor=tk.CENTER, width=200, height=50)
        entry_password = ttk.Entry(self, font="Verdana")
        entry_password.\
            place(x=300, y=400, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="=Log in to see the pictures=", relief=RAISED,
                  command=lambda: switch_to_pictures(entry_user_name, entry_password, self)).\
            place(x=100, y=600, anchor=tk.CENTER, width=200, height=50)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)).\
            place(x=300, y=600, anchor=tk.CENTER, width=200, height=50)


class PicturesPage1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel, storage_pictures, count_pictures, count_five_pictures,\
            BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED
        count_five_pictures = 0
        count_pictures = 0
        tk.Label(self, text="Picture Page1", font=LARGEFONT).\
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Hello client: {USER_NAME}", font=MEDIUM1). \
            place(x=600, y=85, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)).\
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="To upload pictures", relief=RAISED,
                  command=lambda: master.switch_frame(UploadPicturesPage)).\
            place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To Edit pictures", relief=RAISED,
                  command=lambda: master.switch_frame(EditPicturesPage)).\
            place(x=775, y=700, anchor=tk.CENTER, width=350, height=50)
        # command=lambda: master.switch_frame(EditPicturesPage)
        tk.Button(self, text="Go to page2", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=1075, y=700, anchor=tk.CENTER, width=250, height=50)
        # receives the storage of pictures from the server
        if storage_pictures is not None:
            for image in storage_pictures:
                print_pictures(image, self)
                BUTTON_IMAGE = ''
                IF_IMAGE_PRESSED = False
                EDIT_IMAGE = ''
                panel = None
        else:
            tk.Label(self, text="Theres are no pictures in the storage").pack()


class PicturesPage2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel, storage_pictures, count_pictures, count_five_pictures,\
            BUTTON_IMAGE
        count_five_pictures = 0
        count_pictures = 0
        tk.Label(self, text="Picture Page2", font=LARGEFONT).\
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Hello client: {USER_NAME}", font=MEDIUM1). \
            place(x=600, y=85, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)).\
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="To upload pictures", relief=RAISED,
                  command=lambda: master.switch_frame(UploadPicturesPage)).\
            place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To Edit pictures", relief=RAISED,
                  command=lambda: master.switch_frame(EditPicturesPage)).\
            place(x=775, y=700, anchor=tk.CENTER, width=350, height=50)
        # command=lambda: master.switch_frame(EditPicturesPage)
        tk.Button(self, text="Go to page2", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=1075, y=700, anchor=tk.CENTER, width=250, height=50)
        if storage_pictures is not None:
            for image in storage_pictures:
                print_pictures(image, self)
                panel = None
        else:
            tk.Label(self, text="Theres are no pictures in the storage").pack()


class PicturesPage3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel, storage_pictures, count_pictures, count_five_pictures,\
            BUTTON_IMAGE
        count_five_pictures = 0
        count_pictures = 0
        tk.Label(self, text="Picture Page3", font=LARGEFONT).\
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Hello client: {USER_NAME}", font=MEDIUM1). \
            place(x=600, y=85, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)).\
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="To upload pictures", relief=RAISED,
                  command=lambda: master.switch_frame(UploadPicturesPage)).\
            place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To Edit pictures", relief=RAISED,
                  command=lambda: master.switch_frame(EditPicturesPage)).\
            place(x=775, y=700, anchor=tk.CENTER, width=350, height=50)
        # command=lambda: master.switch_frame(EditPicturesPage)
        tk.Button(self, text="Go to page2", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=1075, y=700, anchor=tk.CENTER, width=250, height=50)
        if storage_pictures is not None:
            for image in storage_pictures:
                print_pictures(image, self)
                panel = None
        else:
            tk.Label(self, text="Theres are no pictures in the storage").pack()


class EditPicturesPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global EDIT_IMAGE, panel
        if EDIT_IMAGE == '':
            tk.Label(self, text="No picture was selected", font=MEDIUM1).\
                place(x=600, y=90, anchor=tk.CENTER, width=200, height=40)
        image = EDIT_IMAGE
        tk.Label(self, text=Edit_Pictures_Page, font=LARGEFONT). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=100)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        self.b = tk.Button(self, text="To upload the picture", relief=RAISED, command=lambda: self.sure())
        self.b.place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To download the pictures", relief=RAISED,
                  ). \
            place(x=775, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="Back to Pictures Page1", relief=RAISED,
                  command=lambda: master.switch_frame(PicturesPage1)). \
            place(x=1075, y=700, anchor=tk.CENTER, width=250, height=50)
        if panel is None:
            panel = tk.Label(self, image=image, relief=FLAT)
            panel.image = image
            panel.place(x=200, y=300, anchor=tk.CENTER)
        else:
            panel.configure(image=image)
            panel.image = image
        panel = None
        tk.Button(self, text="Edit function1", relief=RAISED,
                  ). \
            place(x=800, y=150, anchor=tk.CENTER, width=200, height=40)
        ttk.Entry()\
            .place(x=800, y=195, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="Edit function2", relief=RAISED,
                  ). \
            place(x=1100, y=150, anchor=tk.CENTER, width=200, height=40)
        ttk.Entry()\
            .place(x=1100, y=195, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="Edit function3", relief=RAISED,
                  ). \
            place(x=800, y=250, anchor=tk.CENTER, width=200, height=40)
        ttk.Entry()\
            .place(x=800, y=295, anchor=tk.CENTER, width=200, height=25)
        print(f'The image: {image}')

    def sure(self):
        self.b['text'] = "Are you sure?"
        self.b['command'] = lambda: select_image(self, None)


class UploadPicturesPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global NUMBER_PICTURES
        tk.Label(self, text=Upload_pictures_Page, font=LARGEFONT).\
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text="You can upload up to five pictures", font=MEDIUM1).\
            place(x=150, y=640, anchor=tk.CENTER, width=300, height=20)
        tk.Button(self, text="Go to Start Page",
                  command=lambda: master.switch_frame(StartPage)).\
            place(x=100, y=700, anchor=tk.CENTER, width=200, height=50)
        NUMBER_PICTURES = 0
        tk.Button(self, text="Upload", font=MEDIUM2, command=lambda: master.switch_frame(PicturesPage1)). \
            place(x=300, y=700, anchor=tk.CENTER, width=200, height=50)
        select_image_button = tk.Button(self, text="Select Image",
                                        command=lambda: select_image(self, select_image_button))
        select_image_button.place(x=500, y=700, anchor=tk.CENTER, width=200, height=50)


if __name__ == '__main__':
    # local host IP '127.0.0.1'
    # host = '172.20.201.124'
    host = '127.0.0.1'
    port = 42069
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Connected to Server: ", s.getsockname())

        root = MainWindow()
        root.title("Pictures for your day")
        root.minsize(1200, 1150)
        root.mainloop()
    except ConnectionError and ConnectionResetError as err:
        print(f'Something came up: {err}')
    finally:
        s.close()
        quit()
