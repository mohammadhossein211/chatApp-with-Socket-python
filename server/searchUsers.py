import mysql.connector


def searchUsers(txt, notUserId):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1212",
        database="chat_v1"
    )
    users = []
    try:

        mycursor = mydb.cursor()
        sql = f"SELECT id, name, username from users where username like '%{txt}%' and id!={notUserId}"
        mycursor.execute(sql)
        for user in mycursor:
            users.append({
                "userId": user[0],
                "name": user[1],
                "username": user[2]
            })
        return users
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    return users
