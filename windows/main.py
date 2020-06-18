import socket
import pickle
import sys
from PyQt5.QtWidgets import *
from windows.chat import *


f = open("port.txt", "r")
port = int(f.read())


class Main(QWidget):
    def __init__(self, userId):
        super().__init__()
        self.setGeometry(100, 100, 300, 450)
        # self.setWindowTitle("Hi, ".data["data"][""])
        self.UI(userId)

    def UI(self, userId):
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
        chatListNames = []

        for i in range(len(self.chatList)):
            chatListNames.append(self.chatList[i]["name"])

        name = dataRes["data"]["name"]
        self.setWindowTitle(f"Hi, {name}")

        self.namesListWidget = QListWidget(self)
        self.namesListWidget.addItems(chatListNames)
        self.namesListWidget.itemClicked.connect(self.openChat)

        formLayout = QFormLayout()
        formLayout.addRow(self.namesListWidget)

        self.setLayout(formLayout)
        self.userId = userId
        self.show()

    def openChat(self, item):
        print(f"item {self.namesListWidget.currentRow()}.{item.text()} clicked!")
        toUserId = self.chatList[self.namesListWidget.currentRow()]["userId"]
        self.chatWindow = Chat(self.userId, toUserId, item.text())
        self.hide()


def opneMainWindow():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())
