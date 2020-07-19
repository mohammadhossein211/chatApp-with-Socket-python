import mysql.connector


def getChats(userId):
    userId_list = []
    tempUserIdList = []
    messages = []

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="m1121212",
            database="chat_v1"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT userId,toUserId from messages where userId={userId} or toUserId={userId} order by time desc"
        mycursor.execute(sql)
        for x in mycursor:
            if x[0] != userId and x[0] not in userId_list:
                userId_list.append(x[0])
            if x[1] != userId and x[1] not in userId_list:
                userId_list.append(x[1])
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    chat_list = []
    if len(userId_list) != 0:
        for i in range(len(userId_list)):
            try:
                mycursor = mydb.cursor()
                sql = f"SELECT id,name, username FROM chat_v1.users where id={userId_list[i]}"
                mycursor.execute(sql)
                for x in mycursor:
                    chat_list.append(
                        {"userId": x[0], "name": x[1], "username": x[2]})
                    break
                # print("New user registered with id: ", mycursor.lastrowid)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))

    return chat_list
