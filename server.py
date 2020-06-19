import socket
import time
import pickle
import mysql.connector

HEADERSIZE = 10

f = open("port.txt", "r")
port = int(f.read())

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="m1121212",
    database="chat_v1"
)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", port))
s.listen(5)


def main():
    while True:
        serverSocket, address = s.accept()
        msg = serverSocket.recv(1024)
        data = pickle.loads(msg)
        print(data["data"])
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
                serverSocket.send(pickle.dumps(x))
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
                serverSocket.send(pickle.dumps(x))
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
                serverSocket.send(pickle.dumps(x))
        elif(data["for"] == "getChats"):
            userId = data["data"]["userId"]
            chats_list_names = getChats(userId)
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
                    "chatListNames": chats_list_names,
                    "name": name
                },
                "error": ""
            }
            serverSocket.send(pickle.dumps(x))
        elif(data["for"] == "openChat"):
            messages = openChat(data["data"]["userId"],
                                data["data"]["toUserId"])
            if(messages):

                x = {
                    "for": "openChat",
                    "data": {
                        "messages": messages,
                        "toName": getNameOfUser(data["data"]["toUserId"])
                    },
                    "error": ""
                }
            serverSocket.send(pickle.dumps(x))
        elif(data["for"] == "sendMessage"):
            messageTime = sendMessage(
                data["data"]["userId"], data["data"]["toUserId"], data["data"]["text"])
            if(messageTime):
                x = {
                    "for": "sendMessage",
                    "answer": "True",
                    "data": {
                        "time": messageTime
                    },
                    "error": ""
                }
                serverSocket.send(pickle.dumps(x))
            # serverSocket.send(
            #     bytes("Message from server: Hello from server!", "utf-8"))

    s.close()


def sendMessage(userId, toUserId, text):
    messageId = 0
    try:
        mycursor = mydb.cursor()
        sql = f"insert into messages (userId,toUserId,text) values ({userId},{toUserId},'{text}')"
        mycursor.execute(sql)
        mydb.commit()
        messageId = mycursor.lastrowid
        print("message sent with id: ", messageId)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    try:
        mycursor = mydb.cursor()
        sql = f"select time from messages where id={messageId}"
        mycursor.execute(sql)
        for x in mycursor:
            return x[0]
        messageId = mycursor.lastrowid
        print("message sent with id: ", messageId)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    return False


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


def openChat(userId, toUserId):
    messages = []
    try:
        mycursor = mydb.cursor()
        sql = f"SELECT userId,toUserId,text,time from messages where (userId={userId} and toUserId={toUserId}) or (userId={toUserId} and toUserId={userId}) order by messages.time desc limit 0,50"
        mycursor.execute(sql)
        for x in mycursor:
            if x[0] == userId:
                messages.append({
                    "isSent": "True",
                    "isReceived": "False",
                    "text": x[2],
                    "time": x[3]
                })
            else:
                messages.append({
                    "isSent": "False",
                    "isReceived": "True",
                    "text": x[2],
                    "time": x[3]
                })
        return messages
        # print("New user registered with id: ", mycursor.lastrowid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    return False


def getChats(userId):
    userId_list = []
    tempUserIdList = []
    messages = []
    try:
        mycursor = mydb.cursor()
        sql = f"SELECT userId,toUserId from messages where userId={userId} or toUserId={userId} order by time desc"
        mycursor.execute(sql)
        for x in mycursor:
            if x[0] != userId and x[0] not in userId_list:
                userId_list.append(x[0])
            if x[1] != userId and x[1] not in userId_list:
                userId_list.append(x[1])
                # tempUserIdList.append(x[0])
                # messages.append({"userId": x[0], "time": x[1]})
        # print("New user registered with id: ", mycursor.lastrowid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    # try:
    #     mycursor = mydb.cursor()
    #     sql = f"SELECT toUserId,time from messages where userId={userId} or toUserId={userId} order by time desc"
    #     mycursor.execute(sql)
    #     for x in mycursor:
    #         if x[0] != userId and x[0] not in tempUserIdList:
    #             tempUserIdList.append(x[0])
    #             messages.append({"userId": x[0], "time": x[1]})
    #     # print("New user registered with id: ", mycursor.lastrowid)
    # except mysql.connector.Error as err:
    #     print("Something went wrong: {}".format(err))

    # n = len(messages)

    # for i in range(n-1):
    #     for j in range(0, n-i-1):
    #         if messages[j]["time"] < messages[j+1]["time"]:
    #             messages[j], messages[j +
    #                                   1] = messages[j+1], messages[j]

    # for i in range(len(messages)):
    #     userId_list.append(messages[i]["userId"])

    chat_list = []
    if len(userId_list) != 0:
        for i in range(len(userId_list)):
            try:
                mycursor = mydb.cursor()
                sql = f"SELECT id,name FROM chat_v1.users where id={userId_list[i]}"
                mycursor.execute(sql)
                for x in mycursor:
                    chat_list.append({"userId": x[0], "name": x[1]})
                    break
                # print("New user registered with id: ", mycursor.lastrowid)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))

    return chat_list


def login(data):
    userId = 0
    try:
        mycursor = mydb.cursor()
        y = data["username"]
        sql = f"SELECT id,name,username,password FROM users where username='{y}'"
        val = (data["username"])
        mycursor.execute(sql)
        for x in mycursor:
            if x[3] == data["password"]:
                userId = x[0]
                break
        # print("New user registered with id: ", mycursor.lastrowid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    return userId


def register(data):
    answer = {}
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"
        val = (data["name"], data["username"], data["password"])
        mycursor.execute(sql, val)
        mydb.commit()
        print("New user registered with id: ", mycursor.lastrowid)
        answer = {
            "userId": mycursor.lastrowid,
            "error": ""
        }
        return answer
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        answer = {
            "userId": 0,
            "error": err
        }
        return answer
    answer = {
        "userId": 0,
        "error": "Somethin went wrong please try again!"
    }
    return answer


main()
# d = {1: "hi", 2: "there"}
# msg = pickle.dumps(d)
# msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
# print(msg)
# clientsocket.send(msg)
