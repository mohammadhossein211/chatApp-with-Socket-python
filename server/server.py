import socket
import time
import pickle
import mysql.connector
import sendMsg
from openChat import *
from getChats import *
from identify import *
from searchUsers import *


f = open("../port.txt", "r")
port = int(f.read())

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="m1121212",
    database="chat_v1"
)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", port))
s.listen(5)

clients_socket = []


def main():
    while True:
        serverSocket, address = s.accept()

        msg = serverSocket.recv(1024)
        data = pickle.loads(msg)
        print(data["data"])
        x = {
            "answer": "False"
        }
        if(data["for"] == "register"):
            result = register(data["data"])
            if(result["error"] == ""):
                x = {
                    "for": "register",
                    "answer": "True",
                    "data": {
                        "name": data["data"]["name"],
                        "username": data["data"]["username"],
                        "password": data["data"]["password"],
                        "userId": result["userId"]
                    },
                    "error": ""
                }

            else:
                x = {
                    "for": "register",
                    "answer": "False",
                    "data": {
                        "name": data["data"]["name"],
                        "username": data["data"]["username"],
                        "password": data["data"]["password"]
                    },
                    "error": result["error"]
                }
        elif(data["for"] == "login"):
            userId = login(data["data"])
            if(userId):
                # chats_list_names = getChats(userId)
                x = {
                    "for": "login",
                    "answer": "True",
                    "data": {
                        "userId": userId
                    },
                    "error": ""
                }

                clients_socket.append(
                    {"s": serverSocket, "userId": userId})

        elif(data["for"] == "getChats"):
            userId = data["data"]["userId"]
            users = getChats(userId)
            name = ''
            try:
                mycursor = mydb.cursor()
                sql = f"SELECT name FROM users where id={userId}"
                mycursor.execute(sql)
                for x in mycursor:
                    name = x[0]
                    break
                # print("New user registered with id: ", mycursor.lastrowid)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))

            x = {
                "for": "getChats",
                "data": {
                    "users": users,
                    "name": name
                },
                "error": ""
            }

        elif(data["for"] == "openChat"):
            messages = openChat(data["data"]["userId"],
                                data["data"]["toUserId"], 0)
            x = {
                "for": "openChat",
                "data": {
                    "messages": messages,
                    "toName": getNameOfUser(data["data"]["toUserId"])
                },
                "error": ""
            }
        elif(data["for"] == "sendMessage"):
            message = sendMsg.sendMessage(
                data["data"]["userId"], data["data"]["toUserId"], data["data"]["text"])
            if(message["msgId"]):
                x = {
                    "for": "sendMessage",
                    "answer": "True",
                    "data": {
                        "time": message["msgTime"],
                        "msgId": message["msgId"]
                    },
                    "error": ""
                }
        elif(data["for"] == "refreshChat"):
            messages = openChat(data["data"]["userId"],
                                data["data"]["toUserId"],
                                data["data"]["lastMsgId"])
            x = {
                "for": "refreshChat",
                "answer": "True",
                "data": {
                    "messages": messages,
                },
                "error": ""
            }

        elif(data["for"] == "searchUsers"):
            users = searchUsers(data["data"]["txt"], data["data"]["userId"])
            if(users):
                x = {
                    "for": "searchUsers",
                    "answer": "True",
                    "data": {
                        "users": users
                    }
                }

        serverSocket.send(pickle.dumps(x))
    s.close()


def clientsAdd(userId, serverSocket):
    num = 0
    isAdded = False
    for i in range(0, len(clients_socket)):
        if userId == clients_socket[i]["userId"]:
            isAdded = True
            num = i
            clients_socket[i]["s"] = serverSocket
    if not isAdded:
        clients_socket.append(
            {"s": serverSocket, "userId": userId})
        num = -1
    return num


def getNameOfUser(userId):
    try:
        mycursor = mydb.cursor()
        sql = f"SELECT name from users where id={userId}"
        mycursor.execute(sql)
        for x in mycursor:
            return x[0]
        # print("New user registered with id: ", mycursor.lastrowid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    return False


main()
# d = {1: "hi", 2: "there"}
# msg = pickle.dumps(d)
# msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
# print(msg)
# clientsocket.send(msg)
