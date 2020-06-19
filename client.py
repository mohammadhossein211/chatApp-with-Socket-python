import windows.main as mainFile
import windows.chat as chatFile
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
        self.setGeometry(100, 100, 400, 550)
        self.setWindowTitle("Chat App")
        self.UI()

    def UI(self):
        formLayout = QFormLayout()

        self.registerErrorLabel = QLabel("")
        style = "color: red; font-size: 15px"
        self.registerErrorLabel.setStyleSheet(style)

        self.reg_name_input = QLineEdit()
        self.reg_userName_input = QLineEdit()
        self.reg_pass_input = QLineEdit()

        self.registerBtn = QPushButton("Register")
        self.registerBtn.clicked.connect(self.register)

        formLayout.addRow(self.registerErrorLabel)
        formLayout.addRow(QLabel("Name: "), self.reg_name_input)
        formLayout.addRow(QLabel("UserName: "), self.reg_userName_input)
        formLayout.addRow(QLabel("Password: "), self.reg_pass_input)
        formLayout.addRow(self.registerBtn)

        self.loginErrorLabel = QLabel("")
        self.loginErrorLabel.setStyleSheet(style)

        self.login_username_input = QLineEdit()
        self.login_password_input = QLineEdit()
        self.loginBtn = QPushButton("Login")
        self.loginBtn.clicked.connect(self.login)
        formLayout.addRow(self.loginErrorLabel)
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
        self.mainWindow = mainFile.Main(userId)

    def register(self):
        if (len(self.reg_name_input.text()) >= 3 and len(self.reg_userName_input.text()) >= 3 and len(self.reg_pass_input) >= 3):
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
        else:
            self.registerErrorLabel.setText(
                "Please fill all 3 inputs below with at least 3 char")

    def login(self):
        if(len(self.login_username_input.text()) >= 3 and len(self.login_password_input.text()) >= 3):
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
        else:
            self.loginErrorLabel.setText(
                "Please fill all 3 inputs below with at least 3 char")


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
