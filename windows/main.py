import socket
import pickle
import sys
from PyQt5.QtWidgets import *
import windows.chat as chatFile


f = open("port.txt", "r")
port = int(f.read())


class Main(QWidget):
    def __init__(self, userId):
        super().__init__()
        self.setGeometry(100, 100, 400, 550)
        # self.setWindowTitle("Hi, ".data["data"][""])
        self.UI(userId)

    def UI(self, userId):
        self.searchUsers = []
        x = {
            "for": "getChats",
            "data":
            {
                "userId": userId
            }
        }
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", port))
        send = pickle.dumps(x)
        s.send(send)
        msg = s.recv(2048)
        s.close()
        dataRes = pickle.loads(msg)
        self.chatList = dataRes["data"]["chatListNames"]
        self.chatListNames = []

        for i in range(len(self.chatList)):
            self.chatListNames.append(self.chatList[i]["name"])

        name = dataRes["data"]["name"]
        self.setWindowTitle(f"Hi, {name}")

        self.namesListWidget = QListWidget(self)
        self.namesListWidget.addItems(self.chatListNames)
        self.namesListWidget.itemClicked.connect(self.openChat)

        formLayout = QFormLayout()

        self.searchInput = QLineEdit()
        self.searchBtn = QPushButton("search")
        self.searchBtn.clicked.connect(self.searchUser)
        self.allUsersBtn = QPushButton("All Users")
        self.allUsersBtn.clicked.connect(self.backToAllUsers)

        hbox = QHBoxLayout()
        hbox.addWidget(self.searchInput)
        hbox.addWidget(self.searchBtn)
        hbox.addWidget(self.allUsersBtn)
        formLayout.addRow(hbox)
        formLayout.addRow(self.namesListWidget)

        self.setLayout(formLayout)
        self.userId = userId
        self.show()

    def openChat(self, item):
        print(f"item {self.namesListWidget.currentRow()}.{item.text()} clicked!")
        toUserId = self.chatList[self.namesListWidget.currentRow()]["userId"]
        self.chatWindow = chatFile.Chat(self.userId, toUserId, item.text())
        self.hide()

    def searchUser(self):
        if (self.searchInput.text() != ""):
            # x = {
            #     "for": "searchUsers",
            #     "data": {
            #         "username": self.searchInput.text()
            #     }
            # }
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect(("localhost", port))
            # send = pickle.dumps(x)
            # s.send(send)
            # msg = s.recv(2048)
            # s.close()
            # dataRes = pickle.loads(msg)
            # if(dataRes["for"] == "searchUsers"):
            #     if(dataRes["answer"] == "Treu"):
            #         self.searchUsers = dataRes["data"]["users"]
            self.namesListWidget.clear()
        else:
            print("")

    def backToAllUsers(self):
        self.searchInput.setText("")
        self.namesListWidget.clear()
        self.namesListWidget.addItems(self.chatListNames)


def opneMainWindow():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())
