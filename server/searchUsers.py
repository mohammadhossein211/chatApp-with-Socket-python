import mysql.connector


def searchUsers(txt, notUserId):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="m1121212",
        database="chat_v1"
    )
    users = []
    try:

        mycursor = mydb.cursor()
        sql = f"SELECT id, name, username from users where username like '%{txt}%' and id!={notUserId}"
        mycursor.execute(sql)
        for x in mycursor:
            users.append({
                "userId": x[0],
                "name": x[1],
                "username": x[2]
            })
        return users
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    return False
