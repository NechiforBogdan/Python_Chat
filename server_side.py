import socket
import threading

"""
    Gets IP by host name <socket.gethostbyname>
    Sets port number (choice)
    Puts IP & PORT in tuple for binding
        <ADDR>
    Creates socket < socket.socket() > 
        socket() takes 2 param : 
            @AF_IN : Internet Adress family ( AF_INET = IPv4 )
            @SOCK_STREAM : Specifies type of socket ( SOCK_STREAM = TCP  // SOCK_DGRAM = UDP )

"""
HEADER = 1024
PORT = 585
SERVER = "10.4.37.148"  # Gets YOUR IP address (u can type it manually if you want)
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

users = []
usernames = []

print("Host Name : " + socket.gethostname())  # Can be done by using direcly the public IPv4 of the host
print("Host Address : " + SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates TCP IPv4 Socket
server.bind(ADDR)  # Binds IP & PORT
server.listen()
print(f"Server listening on : {SERVER}")


def broadcast(message):
    for client in users:
        client.send(message)


def handling(client):
    connected = True
    while connected:
        try:
            message = client.recv(HEADER)
            if message.decode(FORMAT).split(">")[1] == "EXIT":
                message_disconnected = f"user {message.decode(FORMAT).split('>')[0]} has disconnected."
                broadcast(message_disconnected.encode(FORMAT))
                index = 0
                for i in range(0, len(users)):
                    if users[i] == client:
                        index = i
                        users.remove(users[i])
                username = usernames[index]
                usernames.remove(username)
                print(f"User '{username}' has disconnected!")
                connected = False
                break
            broadcast(message)
        except:
            if connected:
                print("An error has occurred!")
                break
            else:
                pass
                break
    client.close()
    return 0


"""
    Server listens for any connections until some connects:
        when some1 connects the server stores < server.accept() >:
            store their port & IP in < address > and the information about them (obj) in the < connection >
    !!!server.accept is a "blocker" : stays on same line until connection occurs!!!

"""


def start():
    while True:
        client, address = server.accept()  # accepts all clients onto the server
        # client =  <socket.socket fd=1244, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=
        # ('192.168.1.11', 585), raddr=('192.168.1.11', 55547)>
        # address =  ('192.168.1.11', 55547)
        client.send("USER".encode(FORMAT))
        username = client.recv(HEADER).decode(FORMAT)
        usernames.append(username)
        print(f"{address} has connected with the username {username}")
        broadcast(f"{username} has connected.".encode(FORMAT))
        users.append(client)

        thread = threading.Thread(target=handling, args=(client,))  # Creates & sends thread to client_mungling
        thread.start()

        print(f"Number of active clients : {threading.active_count() - 1}")  # -1 because it has to exclude the host


print("Server is starting...")
start()
