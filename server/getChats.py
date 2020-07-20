import mysql.connector


def getChats(userId):
    userId_list = []

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1212",
            database="chat_v1"
        )
        mycursor = mydb.cursor()
        sql = f"SELECT userId,toUserId from messages where userId={userId} or toUserId={userId} order by time desc"
        mycursor.execute(sql)
        for msg in mycursor:
            if msg[0] != userId and msg[0] not in userId_list:
                userId_list.append(msg[0])
            if msg[1] != userId and msg[1] not in userId_list:
                userId_list.append(msg[1])
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    chat_list = []
    if len(userId_list) != 0:
        for i in range(len(userId_list)):
            try:
                mycursor = mydb.cursor()
                sql = f"SELECT id,name, username FROM chat_v1.users where id={userId_list[i]}"
                mycursor.execute(sql)
                for user in mycursor:
                    chat_list.append(
                        {"userId": user[0], "name": user[1], "username": user[2]})
                    break
                # print("New user registered with id: ", mycursor.lastrowid)
            except mysql.connector.Error as err:
                print("Something went wrong: {}".format(err))

    return chat_list
