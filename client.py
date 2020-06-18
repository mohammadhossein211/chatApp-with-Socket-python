from windows.main import Main
import os
import socket
import pickle
import sys
from PyQt5.QtWidgets import *

f = open("port.txt", "r")
port = int(f.read())

HEADERSIZE = 10


class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 450)
        self.setWindowTitle("Chat App")
        self.UI()

    def UI(self):
        formLayout = QFormLayout()

        self.reg_name_input = QLineEdit()
        self.reg_userName_input = QLineEdit()
        self.reg_pass_input = QLineEdit()

        self.registerBtn = QPushButton("Register")
        self.registerBtn.clicked.connect(self.register)

        formLayout.addRow(QLabel("Name: "), self.reg_name_input)
        formLayout.addRow(QLabel("UserName: "), self.reg_userName_input)
        formLayout.addRow(QLabel("Password: "), self.reg_pass_input)
        formLayout.addRow(self.registerBtn)

        self.loginBtn = QPushButton("Login")
        self.loginBtn.clicked.connect(self.login)

        self.login_username_input = QLineEdit()
        self.login_password_input = QLineEdit()
        formLayout.addRow(QLabel("UserName: "), self.login_username_input)
        formLayout.addRow(QLabel("Password: "), self.login_password_input)
        formLayout.addRow(self.loginBtn)

        self.errorTxt = QLabel()
        formLayout.addRow(self.errorTxt)

        self.setLayout(formLayout)
        self.setWindowTitle("Chats")
        self.show()

    def chats(self, userId):
        self.hide()
        self.mainWindow = Main(userId)
        print("HHHHHHHHHH")
        # formLayout = QFormLayout()
        # self.clearMask()

        # self.chats = []  # QPushButton("Register")
        # btn = QPushButton("Open Chat")
        # label = QLabel("Name")
        # x = {"btn": btn, "label": label}
        # self.chats.append(x)
        # for i in range(0, len(self.chats)):
        #     self.chats[i]["btn"].clicked.connect(self.openChat)
        #     formLayout.addRow(self.chats[i]["label"], self.chats[i]["btn"])

    def openChat(self):
        return True

    def register(self):
        if True or(self.reg_name_input.text() != "" and self.reg_userName_input.text() != "" and self.reg_pass_input != ""):
            x = {
                "for": "register",
                "data":
                    {
                        "name": self.reg_name_input.text(),
                        "username": self.reg_userName_input.text(),
                        "password": self.reg_pass_input.text()
                    }
            }
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", port))
            send = pickle.dumps(x)
            s.send(send)
            msg = s.recv(2048)
            dataRes = pickle.loads(msg)
            s.close()
            if(dataRes["for"] == "register"):
                if(dataRes["answer"] == "True"):
                    # self.hide()
                    self.chats(dataRes["data"]["userId"])
                else:
                    self.errorTxt.text = dataRes["error"]

    def login(self):
        if(self.login_username_input.text() != "" and self.login_password_input.text() != ""):
            x = {
                "for": "login",
                "data": {
                    "username": self.login_username_input.text(),
                    "password": self.login_password_input.text()
                }
            }
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", port))
            send = pickle.dumps(x)
            s.send(send)
            msg = s.recv(2048)
            dataRes = pickle.loads(msg)
            s.close()
            if(dataRes["for"] == "login"):
                if(dataRes["answer"] == "True"):
                    # self.hide()
                    self.chats(dataRes["data"]["userId"])


def registerAndLoginWindow():
    App = QApplication(sys.argv)
    window = Home()
    sys.exit(App.exec_())


if __name__ == "__main__":
    registerAndLoginWindow()

# while True:
#     full_msg = b''
#     new_msg = True
#     while True:
#         msg = s.recv(16)
#         if new_msg:
#             print("new msg len:", msg[:HEADERSIZE])
#             msglen = int(msg[:HEADERSIZE])
#             new_msg = False

#         print(f"full message length: {msglen}")

#         full_msg += msg

#         print(len(full_msg))

#         if len(full_msg)-HEADERSIZE == msglen:
#             print("full msg recvd")
#             print(full_msg[HEADERSIZE:])
#             print(pickle.loads(full_msg[HEADERSIZE:]))
#             new_msg = True
#             full_msg = b""
