import windows.main as mainFile
import windows.chat as chatFile
import os
import socket
import pickle
import sys
import sendMsg
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
        self.login_username_input.setText("maryam")
        self.login_password_input = QLineEdit()
        self.login_password_input.setText("1234")
        self.loginBtn = QPushButton("Login")
        self.loginBtn.clicked.connect(self.login)
        formLayout.addRow(self.loginErrorLabel)
        formLayout.addRow(QLabel("UserName: "), self.login_username_input)
        formLayout.addRow(QLabel("Password: "), self.login_password_input)

        formLayout.addRow(self.loginBtn)

        self.errorTxt = QLabel()
        formLayout.addRow(self.errorTxt)

        self.setLayout(formLayout)
        self.setWindowTitle("Home")
        self.show()

    def chats(self, userId):
        self.hide()
        self.mainWindow = mainFile.Main(userId)

    def register(self):
        if (len(self.reg_name_input.text()) >= 3 and len(self.reg_userName_input.text()) >= 3 and len(self.reg_pass_input.text()) >= 3):
            x = {
                "for": "register",
                "data":
                    {
                        "name": self.reg_name_input.text(),
                        "username": self.reg_userName_input.text(),
                        "password": self.reg_pass_input.text()
                    }
            }

            dataRes = sendMsg.sendData(x)
            if(dataRes["answer"] == "True"):
                self.chats(dataRes["data"]["userId"])
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
            dataRes = sendMsg.sendData(x)
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
