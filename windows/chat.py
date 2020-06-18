import socket
import pickle
import sys
from PyQt5.QtWidgets import *

f = open("port.txt", "r")
port = int(f.read())


class Chat(QWidget):
    def __init__(self, userId, toUserId, toName):
        super().__init__()
        self.setGeometry(100, 100, 300, 450)
        # self.setWindowTitle("Hi, ".data["data"][""])
        self.UI(userId, toUserId, toName)

    def UI(self, userId, toUserId, toName):
        x = {
            "for": "openChat",
            "data":
            {
                "userId": userId,
                "toUserId": toUserId
            }
        }
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", port))
        send = pickle.dumps(x)
        s.send(send)
        msg = s.recv(10000)
        s.close()

        dataRes = pickle.loads(msg)

        toName = toName
        try:
            toName = dataRes['data']['toName']
        except:
            pass
        self.setWindowTitle(f"{toName}'s Chat")

        self.messagesList = dataRes["data"]["messages"]
        messagesTextList = []

        for i in range(len(self.messagesList)):
            text = self.messagesList[i]["text"]
            time = str(self.messagesList[i]["time"])
            messagesTextList.append(f"{text}\n{time}")

        self.messagesListWidget = QListWidget(self)
        self.messagesListWidget.addItems(messagesTextList)
        self.messagesListWidget.itemClicked.connect(self.messageClicked)

        # self.chatList = dataRes["data"]["chatListNames"]
        # chatListNames = []

        # for i in range(len(self.chatList)):
        #     chatListNames.append(self.chatList[i]["name"])

        # name = dataRes["data"]["name"]
        # self.setWindowTitle(f"Hi, {name}")

        # self.namesListWidget = QListWidget(self)
        # self.namesListWidget.addItems(chatListNames)
        # self.namesListWidget.itemClicked.connect(self.openChat)

        formLayout = QFormLayout()
        formLayout.addRow(self.messagesListWidget)

        self.setLayout(formLayout)
        # self.userId = userId
        self.show()

    def messageClicked(self, item):
        print(
            f"message {self.messagesListWidget.currentRow()}.{item.text()} clicked!")


def opneChatWindow():
    App = QApplication(sys.argv)
    window = Chat()
    sys.exit(App.exec_())
