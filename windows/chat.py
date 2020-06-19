import socket
import pickle
import sys
from PyQt5.QtWidgets import *
import windows.main as mainFile
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

f = open("port.txt", "r")
port = int(f.read())


class Chat(QWidget):
    def __init__(self, userId, toUserId, toName):
        super().__init__()
        self.setGeometry(100, 100, 400, 550)
        # self.setWindowTitle("Hi, ".data["data"][""])
        self.UI(userId, toUserId, toName)

    def UI(self, userId, toUserId, toName):
        self.userId = userId
        self.toUserId = toUserId
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
        self.messagesListWidget = QListWidget(self)

        for i in range(len(self.messagesList)):
            text = self.messagesList[i]["text"]
            time = str(self.messagesList[i]["time"])
            user = "you"
            # brush = QBrush()
            color = QColor("#ffffff")
            # color.setHsv(0, 0, 100)
            if(self.messagesList[i]["isSent"] == "False"):
                user = toName
                color = QColor("#ddd")
            # brush.setColor(color)
            messagesTextList.append(f"{user}: {text}\n{time[11:-3]}")
            item = QListWidgetItem()
            item.setText(messagesTextList[-1])
            item.setBackground(color)
            self.messagesListWidget.addItem(item)

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
        self.backBtn = QPushButton("Back")
        self.backBtn.clicked.connect(self.backToMain)
        self.message_input = QLineEdit()
        self.sendBtn = QPushButton("Send")
        self.sendBtn.clicked.connect(self.sendMessage)
        formLayout.addRow(self.backBtn)
        formLayout.addRow(self.message_input, self.sendBtn)
        formLayout.addRow(self.messagesListWidget)

        self.setLayout(formLayout)
        # self.userId = userId
        self.show()

    def backToMain(self):
        self.hide()
        userId = self.userId
        self.mainWindow = mainFile.Main(userId)

    def sendMessage(self):
        if (self.message_input.text() != ""):
            x = {
                "for": "sendMessage",
                "data": {
                    "userId": self.userId,
                    "toUserId": self.toUserId,
                    "text": self.message_input.text()
                }
            }
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", port))
            send = pickle.dumps(x)
            s.send(send)
            msg = s.recv(10000)
            s.close()
            dataRes = pickle.loads(msg)
            if(dataRes["answer"] == "True"):
                self.messagesListWidget.insertItem(0,
                                                   f"{self.message_input.text()}\n{dataRes['data']['time']}")
                self.message_input.setText("")

    def messageClicked(self, item):
        print(
            f"message {self.messagesListWidget.currentRow()}.{item.text()} clicked!")


def opneChatWindow():
    App = QApplication(sys.argv)
    window = Chat()
    sys.exit(App.exec_())
