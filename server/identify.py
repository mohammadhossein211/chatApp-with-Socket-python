import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="m1121212",
    database="chat_v1"
)


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
