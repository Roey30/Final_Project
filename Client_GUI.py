import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk


NUMBER = 1
LARGEFONT = ("Verdana", 35)
dictionary = {"Home Page": 1, 'Go to Page1 - To Login': 2, '"Log in to see pictures"': 3, "Pictures Page": 4,
              "Edit Pictures Page": 5, "Upload Pictures Page": 6, 'GoodBye - To exit': 7}
Home_Page = "Home Page"
Sign_in_Page = "Go to Page1 - To Login"
Log_in_Page = "Log in to see pictures"
Pictures_Page = "Pictures Page"
Edit_Pictures_Page = "Edit Pictures Page"
Upload_pictures_Page = "Upload Pictures Page"
exit_button = 'GoodBye - To exit'

storage_user_name = []
storage_password = []
storage_pictures = []
user_name = ''
password = ''


panel = None


def exit_window(button_value):
    global NUMBER, root
    print(button_value)
    print(f"Button pressed: {button_value} with the value: {dictionary[button_value]} ")
    if dictionary[button_value] == 7:
        print("GoodBye")
        root.quit()


def show_text(entry_user_name, entry_password, frame):
    global user_name, password
    user_name = entry_user_name.get()
    password = entry_password.get()
    if user_name == '' or password == '':
        tk.Label(frame, text="Something went wrong please try again").pack()
    else:
        tk.Label(frame, text=f"Your user name is: |{user_name}|").pack()
        print(f"The user |{user_name}| signed in")
        tk.Label(frame, text=f"Your password is: |{password}|").pack()
        print(f"With the password |{password}|")
        storage_user_name.append(user_name)
        storage_password.append(password)
    print(storage_user_name)
    print(storage_password)


def select_image(frame):
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            global panel
            image = Image.open(file_path)
            image = image.resize((150, 150), Image.LANCZOS)
            image = ImageTk.PhotoImage(image)

            if panel is None:
                panel = tk.Label(frame, image=image)
                panel.image = image
                storage_pictures.append(image)
                panel.pack(side="bottom", fill="both", expand=2)
            else:
                panel.configure(image=image)
                panel.image = image
        except Exception as e:
            messagebox.showerror("Error", "Failed to open image\n{}".format(e))
    panel = None


def reset_pictures(frame):
    global storage_pictures
    storage_pictures = None
    tk.Label(frame, text="All the storage got reset").pack()


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
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Start Page").pack()
        tk.Button(self, text=Sign_in_Page, command=lambda: master.switch_frame(SignInPage)).pack()
        tk.Button(self, text=Log_in_Page, command=lambda: master.switch_frame(LogInPage)).pack()
        tk.Button(self, text=Pictures_Page, command=lambda: master.switch_frame(PicturesPage)).pack()
        tk.Button(self, text=Upload_pictures_Page, command=lambda: master.switch_frame(UploadPicturesPage)).pack()
        tk.Button(self, text=exit_button, command=lambda: exit_window(exit_button)).pack()
        tk.Button(self, text="Reset pictures", command=lambda: reset_pictures(self)).pack()


class SignInPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Page 1").pack()
        tk.Label(self, text=f"Please enter User Name:").pack()
        entry_user_name = tk.Entry(self)
        entry_user_name.pack()
        tk.Label(self, text=f"Please enter PassWord").pack()
        entry_password = tk.Entry(self)
        entry_password.pack()
        tk.Button(self, text="Go to Start Page", command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="Sign In", command=lambda: show_text(entry_user_name, entry_password, self)).pack()


class LogInPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text=Log_in_Page).pack()
        tk.Button(self, text="Go to Start Page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class PicturesPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global panel
        tk.Label(self, text=Pictures_Page).pack()
        tk.Button(self, text="Go to Start Page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        print(storage_pictures)
        if storage_pictures is not None:
            for image in storage_pictures:
                if panel is None:
                    panel = tk.Label(self, image=image)
                    panel.image = image
                    panel.pack(side="bottom", fill="both", expand=2)
                else:
                    panel.configure(image=image)
                    panel.image = image
                panel = None
        else:
            tk.Label(self, text="Theres are no pictures in the storage").pack()


class EditPicturesPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text=Edit_Pictures_Page).pack()
        tk.Button(self, text="Go to Start Page",
                  command=lambda: master.switch_frame(StartPage)).pack()


class UploadPicturesPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text=Upload_pictures_Page).pack()
        tk.Button(self, text="Go to Start Page",
                  command=lambda: master.switch_frame(StartPage)).pack()
        select_image_button = tk.Button(self, text="Select Image", command=lambda: select_image(self))
        select_image_button.pack(side="top", fill="x", pady=10)


if __name__ == '__main__':
    root = MainWindow()
    root.title("Pictures for your day")
    root.mainloop()
