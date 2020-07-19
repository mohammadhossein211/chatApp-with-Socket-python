import mysql.connector


def sendMessage(userId, toUserId, text):
    msg = {"msgId": 0, "msgTime": ""}
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="m1121212",
            database="chat_v1"
        )
        mycursor = mydb.cursor()
        sql = f"insert into messages (userId,toUserId,text) values ({userId},{toUserId},'{text}')"
        mycursor.execute(sql)
        mydb.commit()
        msg["msgId"] = mycursor.lastrowid
        mydb.close()
        print("message sent with id: ", msg["msgId"])
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="m1121212",
            database="chat_v1"
        )
        mycursor = mydb.cursor()
        sql = f"select time from messages where id={msg['msgId']}"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        mydb.close()
        for x in myresult:
            msg["msgTime"] = x[0]
            return msg
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    return msg
