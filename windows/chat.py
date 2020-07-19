import socket
import pickle
import sys
from PyQt5.QtWidgets import *
import windows.main as mainFile
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
import sendMsg

f = open("port.txt", "r")
port = int(f.read())


class Chat(QWidget):
    def __init__(self, userId, toUserId, toName):
        super().__init__()
        self.setGeometry(100, 100, 400, 550)
        # self.setWindowTitle("Hi, ".data["data"][""])
        self.lastMsgId = 0
        self.messagesTextList = []
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

        dataRes = sendMsg.sendData(x)
        if toName:
            self.toName = toName
        else:
            self.toName = ""
        try:
            self.toName = dataRes['data']['toName']
        except:
            pass
        self.setWindowTitle(f"{toName}'s Chat")

        self.messagesListWidget = QListWidget(self)
        self.messagesListWidget.itemClicked.connect(self.messageClicked)

        self.setChat(dataRes["data"])

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
        backBtn = QPushButton("Back")
        backBtn.clicked.connect(self.backToMain)
        formLayout.addRow(backBtn)

        self.message_input = QLineEdit()
        formLayout.addRow(self.message_input)

        sendBtn = QPushButton("Send")
        sendBtn.clicked.connect(self.sendMessage)
        # formLayout.addRow(sendBtn)

        refreshBtn = QPushButton("Refresh")
        refreshBtn.clicked.connect(self.refreshChat)
        formLayout.addRow(sendBtn, refreshBtn)

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

            dataRes = sendMsg.sendData(x)
            if(dataRes["answer"] == "True"):
                text = self.message_input.text()
                time = str(dataRes['data']['time'])
                self.messagesListWidget.insertItem(
                    0, f"you: {text}\n{time[11:-3]}")
                self.message_input.setText("")
                self.lastMsgId = dataRes["data"]["msgId"]

    def messageClicked(self, item):
        print(
            f"message {self.messagesListWidget.currentRow()}.{item.text()} clicked!")

    def refreshChat(self):
        x = {
            "for": "refreshChat",
            "data": {
                "userId": self.userId,
                "toUserId": self.toUserId,
                "lastMsgId": self.lastMsgId
            }
        }
        dataRes = sendMsg.sendData(x)
        if(dataRes["answer"] == "True"):
            self.setChat(dataRes["data"])

    def setChat(self, data):
        messagesList = data["messages"]
        self.messagesTextList = []
        if(messagesList):
            self.lastMsgId = messagesList[-1]["msgId"]
            for i in range(len(messagesList)):
                text = messagesList[i]["text"]
                time = str(messagesList[i]["time"])
                user = "you"
                # brush = QBrush()
                color = QColor("#ffffff")
                # color.setHsv(0, 0, 100)
                if(messagesList[i]["isSent"] == "False"):
                    user = self.toName
                    color = QColor("#ddd")
                # brush.setColor(color)
                self.messagesTextList.append(f"{user}: {text}\n{time[11:-3]}")
                item = QListWidgetItem()
                item.setText(self.messagesTextList[-1])
                item.setBackground(color)
                self.messagesListWidget.insertItem(0, item)


def opneChatWindow():
    App = QApplication(sys.argv)
    window = Chat()
    sys.exit(App.exec_())
