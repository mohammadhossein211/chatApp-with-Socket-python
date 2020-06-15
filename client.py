import socket
import pickle
import sys
from PyQt5.QtWidgets import *

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 1243))


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

        self.setLayout(formLayout)
        self.show()

    def register(self):
        if (self.reg_name_input.text() != "" and self.reg_userName_input.text() != "" and self.reg_pass_input != ""):
            print(self.reg_userName_input.text())


def main():
    App = QApplication(sys.argv)
    window = Home()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()

while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new msg len:", msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
