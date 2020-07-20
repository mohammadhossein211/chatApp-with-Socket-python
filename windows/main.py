import socket
import pickle
import sys
from PyQt5.QtWidgets import *
import windows.chat as chatFile
import sendMsg


f = open("port.txt", "r")
port = int(f.read())


class Main(QWidget):
    def __init__(self, userId):
        super().__init__()
        self.setGeometry(100, 100, 400, 550)
        # self.setWindowTitle("Hi, ".data["data"][""])
        self.isInSearch = False
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

        dataRes = sendMsg.sendData(x)

        self.chatList = dataRes["data"]["users"]
        self.savedUsers = self.chatList
        chatListNames = []

        for user in self.chatList:
            chatListNames.append(user["name"])

        name = dataRes["data"]["name"]
        self.setWindowTitle(f"Hi, {name}")

        self.namesListWidget = QListWidget(self)
        self.namesListWidget.addItems(chatListNames)
        self.namesListWidget.itemClicked.connect(self.openChat)

        formLayout = QFormLayout()

        self.searchInput = QLineEdit()
        self.searchBtn = QPushButton("search")
        self.searchBtn.clicked.connect(self.searchUser)
        self.allUsersBtn = QPushButton("Show all my chatss")
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
        id = self.namesListWidget.currentRow()
        toUserId = self.chatList[id]["userId"]
        self.chatWindow = chatFile.Chat(self.userId, toUserId, item.text())
        if self.isInSearch:
            user = self.chatList[id]
            self.savedUsers.append(user)
            self.namesListWidget.addItem(user["name"])
            self.chatList = []
            self.chatList.append(user)
        self.hide()

    def searchUser(self):
        if (self.searchInput.text() != ""):
            x = {
                "for": "searchUsers",
                "data": {
                    "txt": self.searchInput.text(),
                    "userId": self.userId
                }
            }
            dataRes = sendMsg.sendData(x)
            if(dataRes["answer"][0].lower() == "t"):
                self.chatList = dataRes["data"]["users"]
                self.isInSearch = True
                self.namesListWidget.clear()
                for user in self.chatList:
                    self.namesListWidget.addItem(user["name"])

        else:
            print("")

    def backToAllUsers(self):
        self.searchInput.setText("")
        self.namesListWidget.clear()
        chatListNames = []
        for user in self.savedUsers:
            chatListNames.append(user["name"])
        self.chatList = self.savedUsers
        self.namesListWidget.addItems(chatListNames)


def opneMainWindow():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())
