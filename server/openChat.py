import mysql.connector


def openChat(userId, toUserId, lastMsgId):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1212",
        database="chat_v1"
    )
    messages = []
    try:

        sql = f"SELECT userId,toUserId,text,time,id from messages where ((userId={userId} and toUserId={toUserId}) or (userId={toUserId} and toUserId={userId})) and id>{lastMsgId} order by messages.time"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0] == userId:
                messages.append({
                    "isSent": "True",
                    "isReceived": "False",
                    "text": x[2],
                    "time": x[3],
                    "msgId": x[4]
                })
            else:
                messages.append({
                    "isSent": "False",
                    "isReceived": "True",
                    "text": x[2],
                    "time": x[3],
                    "msgId": x[4]
                })
        mydb.close()
        return messages
        # print("New user registered with id: ", mycursor.lastrowid)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    return False
