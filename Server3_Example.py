#!/usr/bin/env python3
import io
import socket
import pickle
import tempfile
from _thread import *
from PIL import Image
import sqlite3


# The client sends:
# sends the username and the password to server for storage them in the DataBase
# sends the username and the password to the sever for checking them in the DataBase
# The client sends the picture to the server to his DataBase


# The server sends:
# confirmation for the login (if the user and the password are indeed in the DataBase)
# receives the storage of pictures from the server

password_storage = []  # pa
username_storage = []  # us
pictures_storage = []  # pi

pictures_to_server_protocol = 'ptsp'
pictures_to_client_protocol = 'ptcp'
log_in_client_protocol = 'LICP'
sign_in_client_protocol = 'SICP'
exist_check_protocol = 'ECP'

gDict = {}
userDict = {}


def sign_in(username, password, c):
    exist = exist_signin_check(username)
    if exist == 'True':
        c.sendall(pickle.dumps('True'))
    elif exist == 'False':
        c.sendall(pickle.dumps('False'))
        userDict[c] = username
        connection_data = sqlite3.connect("username_password_storage.db")
        cursor = connection_data.cursor()

        cursor.execute("INSERT INTO username_password_storage (name, password) VALUES (?, ?)", (username, password))
        connection_data.commit()
        connection_data.close()

        password_storage.append(password)
        username_storage.append(username)
        print(f'The username storage: {username_storage}')
        print(f'The password storage: {password_storage}')


def log_in(username, password, c):
    global username_storage, password_storage
    place = 0
    username_password_exist = pickle.dumps('False')
    connection_data = sqlite3.connect("username_password_storage.db")
    cursor = connection_data.cursor()

    cursor.execute("SELECT * FROM username_password_storage")
    users = cursor.fetchall()

    connection_data.close()

    for u in users:
        if username == u[1]:
            print("Username - True")
            if password == users[place][2]:
                print("Password - True")
                username_password_exist = pickle.dumps('True')
                userDict[c] = username
                break
        place += 1
    c.sendall(username_password_exist)


def exist_signin_check(username):
    exist = False
    conn = sqlite3.connect("username_password_storage.db")
    name = conn.cursor()

    name.execute("SELECT * FROM username_password_storage")
    users = name.fetchall()

    for entry_user_name in users:
        if username == entry_user_name[1]:
            exist = True
    if exist:
        conn.close()
        return 'True'
    else:
        conn.close()
        return 'False'


def serverside_picture_handle(c, number_pictures):
    number_pictures = int(number_pictures)
    while number_pictures > 0:
        image_data = b''
        c.sendall(pickle.dumps('ok'))
        while True:
            data = c.recv(1024)
            print(f"\nThe data: {data}")
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
            pictures_storage.append(image_path)
        number_pictures -= 1
        print(pictures_storage)
    c.sendall(pickle.dumps('Finish'))


def clientside_picture_handle(c):
    print("Helllloooo")
    msg_pic_to_client = str(len(pictures_storage))
    not_thing = b'aaaa'
    print(msg_pic_to_client, type(msg_pic_to_client))
    c.sendall(pickle.dumps(msg_pic_to_client))
    print(f"storage paths: {pictures_storage} ")
    for i in pictures_storage:
        with open(i, 'rb') as f:
            image_data = f.read()
            """            print(f"The image: {i}")
            print(f"The image data: {image_data}")"""
        if pickle.loads(c.recv(1024)) == 'ok':
            c.sendall(image_data)
            c.sendall(not_thing)


# receive function


def receive(c):
    try:
        while True:
            # data received from client
            data = c.recv(1024)
            data = pickle.loads(data)
            print(f'The data: {data}')
            # print(f'The data decoded: {data[0].decode()} , {data[1].decode()}')
            if data[0] == log_in_client_protocol:
                log_in(data[1], data[2], c)
            elif data[0] == sign_in_client_protocol:
                sign_in(data[1], data[2], c)
            elif data[0] == pictures_to_server_protocol:
                serverside_picture_handle(c, data[1])
            elif data == pictures_to_client_protocol:
                clientside_picture_handle(c)
            elif data is None:
                print('Bye')
                print(f"{gDict.pop(c)} Has disconnected")
                # lock released on exit
                # print_lock.release()
                exit_thread()
                break

            if not data or data == 'quit':
                print('Bye')
                print(f"{gDict.pop(c)} Has disconnected")
                # lock released on exit
                # print_lock.release()
                exit_thread()
                break
            broadcast(c, data)
    except EOFError as err:
        print(f"Something came up2: {err}")
        print(f"{gDict.pop(c)} Has disconnected")
    finally:
        c.close()


def broadcast(c, data):
    # print(" | ".join(str(i) for i in gDict.values()))

    for connection in gDict:
        # message = f"{userDict[c]} > {data}"
        # connection.sendall(pickle.dumps(f"{userDict[c]} > {data}"))
        # connection.send(message.encode('ascii'))
        print(f"Connection: {gDict.get(connection)} | Data: {data}")
        # print(f"{userDict[c]} send => {data}")


def main():
    # Local host: '127.0.0.1'
    host = '127.0.0.1'
    port = 42069
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket bound to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
    try:
        # a forever loop until client wants to exit
        while True:
            # establish connection with client
            conn, addr = s.accept()
            global gDict
            global userDict
            # Adds Socket / Connection to Dict
            gDict[conn] = addr

            print('Connected to :', addr[0], ':', addr[1])

            # receive(conn)
            start_new_thread(receive, (conn,))
    except ConnectionError and EOFError as err:
        print(f"Something came up : {err}")
        # Keyboard interrupt with CTRL + C, make sure to close active clients first

        # We never reach this line, but it feels good to have it
    finally:
        s.close()
        quit()


if __name__ == '__main__':
    connect_data = sqlite3.connect("username_password_storage.db")
    user = connect_data.cursor()

    user.execute("SELECT * FROM username_password_storage")
    entries = user.fetchall()

    print("ID - Name - password")
    for entry in entries:
        print(f"{entry[0]}: {entry[1]} - {entry[2]}")

    connect_data.close()
    main()
