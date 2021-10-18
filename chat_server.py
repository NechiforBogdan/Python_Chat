import socket
import threading


"""
    Gets IP by host name <socket.gethostbyname>
    Sets port number (choice)
    Puts IP & PORT in tuple for binding
        <ADR>
    Creates socket < socket.socket() > 
        socket() takes 2 param : 
            @AF_IN : Internet Adress family ( AF_INET = IPv4 )
            @SOCK_STREAM : Specifies type of socket ( SOCK_STREAM = TCP  // SOCK_DGRAM = UDP )
        
"""
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = "uft-8"
HEADER = 64
ADR = (SERVER,PORT)
DISCONNECTED = "DISCONNECTED"

print("Host Name : " + socket.gethostname())  # Can be done by using direcly the public IPv4 of the host 
print("Host Address : "+ SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates TCP IPv4 Socket
server.bind(ADR)        # Binds IP & PORT 


def client_mungling(connection,address):
    print(f"Connected bot : {address}")
    connected = True
    while True:
        msg_length = connection.recv(HEADER).decode(FORMAT)     # receiver the size (HEADER) the message must be & decodes it from binary to utf-8
        msg_length = int(msg_length)                            # converts to int ( ObViOuSlY  (-_-)
        message = connection.recv(msg_length).decode(FORMAT)    # actual message received with the proper length and decoded to uft-8
        print(f"User {address} : {message}")
        if message == DISCONNECTED:                             # disconnects user (not to cause problems later)
            connected = False
    connection.close()                                          
    

"""
    Server listens for any connections until some connects:
        when some1 connects the server stores < server.accept() >:
            store their port & IP in < address > and the information about them (obj) in the < connection >
    !!!server.accept is a "blocker" : stays on same line until connection occurs!!!
        

"""
def start():
    server.listen()
    print(f"Server listening : {SERVER}")
    while True:
        connection,address = server.accept() #Blocks & stocks conn & addr
        thread = threading.Thread(target=client_mungling, args=(connection,address)) # Creates & sends thread to client_mungling
        thread.start()

        print(f"Number of active connections : {threading.active_count() - 1}") # -1 because it has to exclude the host

start()