from client import *

f = open("port.txt", "r")
port = int(f.read())


def sendData(x):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", port))
        send = pickle.dumps(x)
        s.send(send)
        msg = s.recv(10000)
        s.close()
        dataRes = pickle.loads(msg)
        return(dataRes)
    except:
        return(False)
