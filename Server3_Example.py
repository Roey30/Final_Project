#!/usr/bin/env python3
import socket
import pickle
from _thread import *

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
password_protocol = 'pa'
username_protocol = 'us'
pictures_protocol = 'pi'
password_exist = '1'
password_not_exist = '2'
username_exist = 'a'
username_not_exist = 'b'

gDict = {}
userDict = {}


def password_handle(protocol, password, c):
    global password_storage, password_exist, password_not_exist
    password_storage.append(password)
    print(f'The password storage: {password_storage}')
    if protocol == password_protocol + 'l':
        for p in password_storage:
            if password == p:
                password_exist = pickle.dumps(password_exist)
                c.sendall(password_exist)
                return
        c.sendall(pickle.dumps(password_not_exist))


def username_handle(protocol, username, c):
    global username_storage, username_not_exist, username_exist
    username_storage.append(username)
    print(f'The username storage: {username_storage}')
    if protocol == username_protocol + 'l':
        for u in username_storage:
            if username == u:
                username_exist = pickle.dumps(username_exist)
                c.sendall(username_exist)
                return
        c.sendall(pickle.dumps(username_not_exist))


def picture_handle(picture):
    pictures_storage.append(picture)
    print(f'The picture storage: {pictures_storage}')


# receive function
def receive(c):
    while True:
        # data received from client
        data = c.recv(1024)
        data = pickle.loads(data)
        print(f'The data: {data}')
        # print(f'The data decoded: {data[0].decode()} , {data[1].decode()}')
        if data[0][0] + data[0][1] == password_protocol:
            password_handle(data[0], data[1], c)
        elif data[0][0] + data[0][1] == username_protocol:
            userDict[c] = data[1]
            username_handle(data[0], data[1], c)
        elif data[0][0] + data[0][1] == pictures_protocol:
            picture_handle(data[1])

        if not data or data == 'quit':
            print('Bye')
            print(f"{gDict.pop(c)} Has disconnected")
            # lock released on exit
            # print_lock.release()
            exit_thread()
            break
        broadcast(c, data)

    c.close()


def broadcast(c, data):
    # print(" | ".join(str(i) for i in gDict.values()))

    for connection in gDict:
        # message = f"{userDict[c]} > {data}"
        # connection.sendall(pickle.dumps(f"{userDict[c]} > {data}"))
        # connection.send(message.encode('ascii'))
        print(f"Connection: {gDict.get(connection)} | Data: {data}")
        print(f"{userDict[c]} send => {data}")


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
    except ConnectionError as err:
        print(f"Something came up : {err}")
        # Keyboard interrupt with CTRL + C, make sure to close active clients first

        # We never reach this line, but it feels good to have it
    finally:
        s.close()
        quit()


if __name__ == '__main__':
    main()
