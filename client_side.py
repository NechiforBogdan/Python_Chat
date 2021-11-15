import socket
import threading

PORT = 585
FORMAT = 'utf-8'
HEADER = 1024
SERVER = "192.168.178.20"
ADDR = (SERVER, PORT)

username = input("Choose a username:")
print(f"Hello {username} welcome to the chat, if you want to quit this chat just type EXIT")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def getMessage():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message == "USER":
                client.send(username.encode(FORMAT))
            else:
                if username == (message.split(">")[0]):
                    pass
                else:
                    print(message)
        except:
            print("Closing connection!\n")
            client.close()
            break


def sendMessage():
    while True:
        inp = input()
        message = f"{username}>{inp}"
        client.send(message.encode(FORMAT))
        if inp == "EXIT":
            client.close()
            quit()


receivingTHREAD = threading.Thread(target=getMessage)
sendingTHREAD = threading.Thread(target=sendMessage)
receivingTHREAD.start()
sendingTHREAD.start()
