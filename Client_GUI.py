import io
import tempfile
from tkinter import messagebox, filedialog, ttk, FLAT, RAISED
import tkinter as tk
from PIL import Image, ImageTk
import socket
import pickle

log_in_client_protocol = 'LICP'
sign_in_client_protocol = 'SICP'
pictures_to_server_protocol = 'ptsp'
pictures_to_client_protocol = 'ptcp'
exist_check_protocol = 'ECP'
reset_all_picture_protocol = 'RAPP'

password_exist = '1'
password_not_exist = '2'
username_exist = 'a'
username_not_exist = 'b'

NUMBER = 1
LARGE_FONT = ("Times New Roman", 35)
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
storage_path_pictures = []
USER_NAME = ''
PASSWORD = ''
count_pictures = 1
count_five_pictures = 0

EDIT_IMAGE = ''
EDIT_IMAGE_PATH = ''
BUTTON_IMAGE = ''
selected_image_to_edit = ''
IF_IMAGE_PRESSED = False
NUMBER_PICTURES = 0

panel = None
ACCESS = False
Upload_picture_button_picture_page = ''
Are_You_Sure_button_edit_page = ''
upload_edit_button = ''
select_image_button = ''


def exit_window(button_value):
    global NUMBER, root
    print(button_value)
    print(f"Button pressed: {button_value} with the value: {dictionary[button_value]} ")
    if dictionary[button_value] == 7:
        print("GoodBye")
        root.quit()


def exist_check():
    if pickle.loads(s.recv(1024)) == 'True':
        return True
    else:
        return False


def signup_function(entry_user_name, entry_password, frame):
    global USER_NAME, PASSWORD
    USER_NAME = entry_user_name.get()
    PASSWORD = entry_password.get()
    msg = sign_in_client_protocol, USER_NAME, PASSWORD
    s.sendall(pickle.dumps(msg))
    if USER_NAME == '' or PASSWORD == '':
        tk.Label(frame, text="Something went wrong please try again", font=MEDIUM1). \
            place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
    elif exist_check():
        tk.Label(frame, text="This user name is taken", font=MEDIUM1). \
            place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
    else:
        tk.Label(frame, text=f"Your user name is: -> {USER_NAME} <-", font=MEDIUM2). \
            place(x=650, y=300, anchor=tk.CENTER, width=240, height=50)
        print(f"Your username -> {USER_NAME}")
        tk.Label(frame, text=f"Your password is: -> {PASSWORD} <-", font=MEDIUM2). \
            place(x=650, y=400, anchor=tk.CENTER, width=240, height=50)
        print(f"With the password -> {PASSWORD} <-")
        # sends the username and the password to server for storage them in the database
        print(f"msg: {msg}")
        storage_user_name.append(USER_NAME)
        storage_password.append(PASSWORD)

    print(f'The username storage: {storage_user_name}')
    print(f'The password storage: {storage_password}')


def select_image(frame, select_image_button_value):
    global NUMBER_PICTURES, EDIT_IMAGE
    if EDIT_IMAGE == '':
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                global panel
                image = Image.open(file_path)
                print(f"image path: {file_path}")
                storage_path_pictures.append(file_path)
                image = image.resize((200, 200), Image.LANCZOS)
                image = ImageTk.PhotoImage(image)
                if panel is None:
                    panel = tk.Label(frame, image=image)
                    panel.image = image
                    # storage_pictures.append(image)
                    panel.place(x=100 + 200 * NUMBER_PICTURES, y=150, anchor=tk.CENTER)
                    NUMBER_PICTURES += 1
                else:
                    panel.configure(image=image)
                    panel.image = image
                panel = None
                if NUMBER_PICTURES > 4:
                    tk.Label(frame, text="You can upload up to five pictures", font=MEDIUM1). \
                        place(x=500, y=500, anchor=tk.CENTER, width=300, height=50)
                    select_image_button_value.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", "Failed to open image\n{}".format(e))
    else:
        # storage_pictures.append(EDIT_IMAGE)
        tk.Button(frame, text="Are you sure you want to upload this?", font=MEDIUM1)
        frame.master.switch_frame(PicturesPage1)


def reset_pictures(frame):
    global storage_pictures
    storage_pictures = None
    msg = reset_all_picture_protocol
    s.sendall(pickle.dumps(msg))
    tk.Label(frame, text="All the storage got reset").pack()


def login_function(entry_user_name, entry_password, frame):
    # sends the username and the password to the sever for checking them in the database
    global ACCESS, USER_NAME
    ACCESS = False
    print(f'User name: {entry_user_name.get()}, Password: {entry_password.get()}')
    msg = log_in_client_protocol, entry_user_name.get(), entry_password.get()
    print(f"The msg: {msg}")
    incorrect_label = tk.Label(frame, text="Your username or password is incorrect", font=MEDIUM1)
    connected_label = tk.Label(frame, text="This user name is already connected", font=MEDIUM1)
    s.sendall(pickle.dumps(msg))
    access = pickle.loads(s.recv(1024))
    if access == 'True':
        print(f'Yes - access = {access}')
        USER_NAME = entry_user_name.get()
        frame.master.switch_frame(PicturesPage1)
    elif access == 'Taken':
        print(f'No - access = {access}')
        incorrect_label.destroy()
        connected_label.place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)
    elif access == 'False':
        print(f'No - access = {access}')
        connected_label.destroy()
        incorrect_label.place(x=300, y=550, anchor=tk.CENTER, width=500, height=50)


def marked_image(image, button_image, frame, path):
    global EDIT_IMAGE, BUTTON_IMAGE, IF_IMAGE_PRESSED, EDIT_IMAGE_PATH, selected_image_to_edit
    selected_image_to_edit = path
    reset_button = tk.Button(frame, text="Resets marked picture", command=lambda: reset_marked_image(reset_button))
    if not IF_IMAGE_PRESSED:
        EDIT_IMAGE = image
        BUTTON_IMAGE = button_image
        BUTTON_IMAGE.config(relief=tk.SOLID, bd=4, bg="#FFC107")
        reset_button.place(x=775, y=660, anchor=tk.CENTER, width=350, height=30)
        IF_IMAGE_PRESSED = True
    else:
        BUTTON_IMAGE.config(relief=FLAT, bd=4, bg="white")
        BUTTON_IMAGE = button_image
        BUTTON_IMAGE.config(relief=tk.SOLID, bd=4, bg="#FFC107")


def reset_marked_image(reset_button):
    global BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED
    EDIT_IMAGE = ''
    BUTTON_IMAGE.config(relief=FLAT, bd=4, bg="white")
    IF_IMAGE_PRESSED = False
    reset_button.destroy()


def print_pictures(image, frame):
    global panel, count_pictures, count_five_pictures, EDIT_IMAGE_PATH, selected_image_to_edit
    EDIT_IMAGE_PATH = image
    path = image
    if EDIT_IMAGE_PATH:
        global panel
        image_PIL = Image.open(path)
        print(f"image path: {image_PIL}")
        image = image_PIL.resize((200, 200), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        print(f"The selected image to edit: {image}")
    if panel is None:
        button_image = tk.Button(frame, image=image, relief=FLAT, bd=4, bg="white",
                                 command=lambda: marked_image(image, button_image, frame, path))
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
    panel = None


def uploads_pictures_to_server(number_pictures, no_picture_selected, frame, page):
    global storage_path_pictures, Upload_picture_button_picture_page, select_image_button, \
        Are_You_Sure_button_edit_page, upload_edit_button

    if number_pictures == 0:
        no_picture_selected.place(x=400, y=665, anchor=tk.CENTER, width=250, height=20)
        return
    else:
        if no_picture_selected is not None:
            no_picture_selected.config(text=f"number of pictures were selected -> {number_pictures} ")
        msg_pic_to_server = pictures_to_server_protocol, str(number_pictures)
        not_thing = b'aaaa'
        s.sendall(pickle.dumps(msg_pic_to_server))
        print(f"storage paths: {storage_path_pictures} ")
        while True:
            for i in storage_path_pictures:
                with open(i, 'rb') as f:
                    image_data = f.read()
                msg_from_server = pickle.loads(s.recv(1024))
                print(f"msg_from_server: {msg_from_server}")
                if msg_from_server == 'ok':
                    s.sendall(image_data)
                    s.sendall(not_thing)
                elif msg_from_server == 'Finish':
                    storage_path_pictures = []
                    if page == "Picture_Page":
                        Upload_picture_button_picture_page.config(state='disabled')
                        select_image_button.config(state='disabled')
                        no_picture_selected.destroy()
                        tk.Label(frame, text="You have successfully uploaded the picture to the server", font=MEDIUM1).\
                            place(x=450, y=665, anchor=tk.CENTER, width=400, height=20)
                    elif page == "Edit_Page":
                        Are_You_Sure_button_edit_page.destroy()
                        upload_edit_button.config(state='disabled')
                        tk.Label(frame, text="You have successfully uploaded the picture to the server", font=MEDIUM1).\
                            place(x=425, y=665, anchor=tk.CENTER, width=400, height=20)
                    return


def get_pictures_from_server():
    msg_pic_to_client = pictures_to_client_protocol
    s.sendall(pickle.dumps(msg_pic_to_client))
    number_pictures = s.recv(1024)
    number_pictures = int(pickle.loads(number_pictures))
    while number_pictures > 0:
        image_data = b''
        s.sendall(pickle.dumps('ok'))
        while True:
            data = s.recv(1024)
            # print(f"\nThe data: {data}")
            if data[-4:][:4] == b'aaaa':
                print("hellllllooooo")
                image_data += data[:-4]
                break
            else:
                image_data += data

        # Convert the image data into an image object
        image = Image.open(io.BytesIO(image_data))

        with tempfile.NamedTemporaryFile(delete=False) as f:
            image.save(f, format='PNG')
            image_path = f.name
            storage_pictures.append(image_path)
        number_pictures -= 1
        print(storage_pictures)
    return


def download_picture(picture_name, frame):
    global storage_pictures, selected_image_to_edit
    if picture_name == '':
        tk.Label(frame, text='You need to enter name first', font=MEDIUM1).\
            place(x=1075, y=665, anchor=tk.CENTER, width=250, height=50)
        return
    folder_path = filedialog.askdirectory()

    # Check if a folder was selected
    if folder_path:
        # Open your picture variable
        picture = Image.open(selected_image_to_edit)

        picture.save(f"{folder_path}/{picture_name}.jpg")


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
        tk.Label(self, text="Start Page - managing and editing photos", font=LARGE_FONT, fg="red"). \
            place(x=600, y=50, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text="For the Clients", font=MEDIUM1, fg="blue"). \
            place(x=600, y=650, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text=Sign_Up_Page, relief=RAISED, fg="yellow",
                  command=lambda: master.switch_frame(SignUpPage)). \
            place(x=200, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text=Log_in_Page, relief=RAISED, fg="green",
                  command=lambda: master.switch_frame(LogInPage)). \
            place(x=600, y=700, anchor=tk.CENTER, width=400, height=50)
        tk.Button(self, text=exit_button, relief=RAISED,
                  command=lambda: exit_window(exit_button)). \
            place(x=1000, y=700, anchor=tk.CENTER, width=400, height=50)


class SignUpPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Sign in section", font=LARGE_FONT). \
            place(x=600, y=100, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Please enter User Name: ", font=MEDIUM1). \
            place(x=100, y=300, anchor=tk.CENTER, width=200, height=50)
        entry_user_name = ttk.Entry(self, font="Verdana")
        entry_user_name. \
            place(x=300, y=300, anchor=tk.CENTER, width=200, height=25)
        tk.Label(self, text=f"Please enter PassWord: ", font=MEDIUM1). \
            place(x=100, y=400, anchor=tk.CENTER, width=200, height=50)
        entry_password = ttk.Entry(self, font="Verdana")
        entry_password. \
            place(x=300, y=400, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="Sign Up", relief=RAISED,
                  command=lambda: signup_function(entry_user_name, entry_password, self)). \
            place(x=100, y=600, anchor=tk.CENTER, width=200, height=50)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=300, y=600, anchor=tk.CENTER, width=200, height=50)


class LogInPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text=Log_in_Page, font=LARGE_FONT). \
            place(x=600, y=100, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Please enter User Name:"). \
            place(x=100, y=300, anchor=tk.CENTER, width=200, height=50)
        entry_user_name = ttk.Entry(self, font="Verdana")
        entry_user_name. \
            place(x=300, y=300, anchor=tk.CENTER, width=200, height=25)
        tk.Label(self, text=f"Please enter Password"). \
            place(x=100, y=400, anchor=tk.CENTER, width=200, height=50)
        entry_password = ttk.Entry(self, font="Verdana")
        entry_password. \
            place(x=300, y=400, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="=Log in to see the pictures=", relief=RAISED,
                  command=lambda: login_function(entry_user_name, entry_password, self)). \
            place(x=100, y=600, anchor=tk.CENTER, width=200, height=50)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=300, y=600, anchor=tk.CENTER, width=200, height=50)


class PicturesPage1(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel, storage_pictures, count_pictures, count_five_pictures, \
            BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED
        count_five_pictures = 0
        count_pictures = 0
        storage_pictures = []
        get_pictures_from_server()
        tk.Label(self, text="Picture Page1", font=LARGE_FONT). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Hello client: {USER_NAME}", font=MEDIUM1). \
            place(x=600, y=85, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="To upload pictures", relief=RAISED,
                  command=lambda: master.switch_frame(UploadPicturesPage)). \
            place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To Edit pictures", relief=RAISED,
                  command=lambda: master.switch_frame(EditPicturesPage)). \
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
        """        tk.Label(self, text="For the Host", font=MEDIUM1). \
            place(x=600, y=615, anchor=tk.CENTER, width=200, height=20)
        reset_picture_button = tk.Button(self, text="Reset pictures", relief=RAISED, state='disabled',
                                         command=lambda: reset_pictures(self))
        reset_picture_button.place(x=600, y=650, anchor=tk.CENTER, width=400, height=50)
        if USER_NAME == 'RoeyFiran':
            reset_picture_button.config(state='active')"""


class PicturesPage2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel, storage_pictures, count_pictures, count_five_pictures, \
            BUTTON_IMAGE, EDIT_IMAGE, IF_IMAGE_PRESSED
        count_five_pictures = 0
        count_pictures = 0
        storage_pictures = []
        get_pictures_from_server()
        tk.Label(self, text="Picture Page1", font=LARGE_FONT). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Hello client: {USER_NAME}", font=MEDIUM1). \
            place(x=600, y=85, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="To upload pictures", relief=RAISED,
                  command=lambda: master.switch_frame(UploadPicturesPage)). \
            place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To Edit pictures", relief=RAISED,
                  command=lambda: master.switch_frame(EditPicturesPage)). \
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
        """        tk.Label(self, text="For the Host", font=MEDIUM1). \
            place(x=600, y=615, anchor=tk.CENTER, width=200, height=20)
        reset_picture_button = tk.Button(self, text="Reset pictures", relief=RAISED, state='disabled',
                                         command=lambda: reset_pictures(self))
        reset_picture_button.place(x=600, y=650, anchor=tk.CENTER, width=400, height=50)
        if USER_NAME == 'RoeyFiran':
            reset_picture_button.config(state='active')"""


class PicturesPage3(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel, storage_pictures, count_pictures, count_five_pictures, \
            BUTTON_IMAGE
        count_five_pictures = 0
        count_pictures = 0
        tk.Label(self, text="Picture Page3", font=LARGE_FONT). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text=f"Hello client: {USER_NAME}", font=MEDIUM1). \
            place(x=600, y=85, anchor=tk.CENTER, width=200, height=20)
        tk.Button(self, text="Go to Start Page", relief=RAISED,
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="To upload pictures", relief=RAISED,
                  command=lambda: master.switch_frame(UploadPicturesPage)). \
            place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)
        tk.Button(self, text="To Edit pictures", relief=RAISED,
                  command=lambda: master.switch_frame(EditPicturesPage)). \
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
        global EDIT_IMAGE, panel, EDIT_IMAGE_PATH, Are_You_Sure_button_edit_page, upload_edit_button
        picture_name = tk.Entry(self, font="Verdana")
        upload_edit_button = tk.Button(self, text="To upload the picture", relief=RAISED, state='disabled',
                                       command=lambda: uploads_pictures_to_server(1, None, self, "Edit_Page"))
        Are_You_Sure_button_edit_page = tk.Button(self, text="Are you sure you want to upload this picture?",
                                                  relief=RAISED,
                                                  command=lambda: (upload_edit_button.config(state="active"),
                                                                   storage_path_pictures.append(EDIT_IMAGE_PATH),
                                                                   print(f"path storage: {storage_path_pictures}"),
                                                                   print(f"The edit image path: {EDIT_IMAGE_PATH}")))
        down_load_picture = tk.Button(self, text="To download the picture", relief=RAISED,
                                      command=lambda: download_picture(picture_name.get(), self))
        down_load_picture.place(x=775, y=700, anchor=tk.CENTER, width=350, height=50)

        Are_You_Sure_button_edit_page.place(x=425, y=665, anchor=tk.CENTER, width=300, height=20)
        upload_edit_button.place(x=425, y=700, anchor=tk.CENTER, width=350, height=50)

        if EDIT_IMAGE == '':
            tk.Label(self, text="No picture was selected", font=MEDIUM1). \
                place(x=600, y=90, anchor=tk.CENTER, width=200, height=40)
            Are_You_Sure_button_edit_page.config(state='disabled')
            upload_edit_button.config(state='disabled')
            down_load_picture.config(state='disabled')
        else:
            tk.Label(self, text="Enter the name of the picture you want", font=MEDIUM1). \
                place(x=775, y=645, anchor=tk.CENTER, width=350, height=20)
            picture_name.place(x=775, y=665, anchor=tk.CENTER, width=350, height=20)
            Are_You_Sure_button_edit_page.config(state='active')
            down_load_picture.config(state='active')
        tk.Label(self, text=Edit_Pictures_Page, font=LARGE_FONT). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=100)
        tk.Button(self, text="Back to Pictures Page1", relief=RAISED,
                  command=lambda: master.switch_frame(PicturesPage1)). \
            place(x=125, y=700, anchor=tk.CENTER, width=250, height=50)
        tk.Button(self, text="Back to Pictures Page1", relief=RAISED,
                  command=lambda: master.switch_frame(PicturesPage1)). \
            place(x=1075, y=700, anchor=tk.CENTER, width=250, height=50)
        if panel is None:
            panel = tk.Label(self, image=EDIT_IMAGE, relief=FLAT)
            panel.image = EDIT_IMAGE
            panel.place(x=200, y=300, anchor=tk.CENTER)
        else:
            panel.configure(image=EDIT_IMAGE)
            panel.image = EDIT_IMAGE
        panel = None
        tk.Button(self, text="Edit function1", relief=RAISED,
                  ). \
            place(x=800, y=150, anchor=tk.CENTER, width=200, height=40)
        ttk.Entry() \
            .place(x=800, y=195, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="Edit function2", relief=RAISED,
                  ). \
            place(x=1100, y=150, anchor=tk.CENTER, width=200, height=40)
        ttk.Entry() \
            .place(x=1100, y=195, anchor=tk.CENTER, width=200, height=25)
        tk.Button(self, text="Edit function3", relief=RAISED,
                  ). \
            place(x=800, y=250, anchor=tk.CENTER, width=200, height=40)
        ttk.Entry() \
            .place(x=800, y=295, anchor=tk.CENTER, width=200, height=25)


class UploadPicturesPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global NUMBER_PICTURES, storage_path_pictures, Upload_picture_button_picture_page, select_image_button
        no_picture_selected = tk.Label(self, text="No picture was selected", font=MEDIUM1)
        tk.Label(self, text=Upload_pictures_Page, font=LARGE_FONT). \
            place(x=600, y=20, anchor=tk.CENTER, width=1200, height=150)
        tk.Label(self, text="You can upload up to five pictures", font=MEDIUM1). \
            place(x=130, y=665, anchor=tk.CENTER, width=250, height=20)
        tk.Button(self, text="Go to Start Page",
                  command=lambda: master.switch_frame(StartPage)). \
            place(x=100, y=700, anchor=tk.CENTER, width=200, height=50)
        select_image_button = tk.Button(self, text="Select Image",
                                        command=lambda: select_image(self, select_image_button))
        Upload_picture_button_picture_page = tk.Button(self, text="Upload", font=MEDIUM2,
                                                       command=lambda: uploads_pictures_to_server
                                                       (NUMBER_PICTURES, no_picture_selected, self, "Picture_Page"))
        Upload_picture_button_picture_page.place(x=300, y=700, anchor=tk.CENTER, width=200, height=50)
        tk.Button(self, text="To pictures page", command=lambda: master.switch_frame(PicturesPage1)). \
            place(x=700, y=700, anchor=tk.CENTER, width=200, height=50)
        NUMBER_PICTURES = 0
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
        root.minsize(1200, 1000)
        root.mainloop()
    except ConnectionError and ConnectionResetError as err:
        print(f'Something came up: {err}')
    finally:
        s.close()
        quit()
