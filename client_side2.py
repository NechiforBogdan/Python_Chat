import socket
import threading

PORT = 585
FORMAT = 'utf-8'
HEADER = 1024
SERVER = "192.168.1.11"
ADDR = (SERVER,PORT)

username = input("Choose a username:")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def getMessage():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message == "USER":
                client.send(username.encode(FORMAT))
            else:
                print(message)
        except:
            print("Error! Closing connection!\n")
            client.close()
            break



def sendMessage():
    while True:
        message = f"{username} : {input('')}"
        client.send(message.encode(FORMAT))



receivingTHREAD = threading.Thread(target=getMessage)
sendingTHREAD = threading.Thread(target=sendMessage)
receivingTHREAD.start()
sendingTHREAD.start()
