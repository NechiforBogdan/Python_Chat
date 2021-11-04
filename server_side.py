import socket
import threading
import encodings.idna


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
HEADER = 64
PORT = 585
SERVER = socket.gethostbyname(socket.gethostname())  # Gets YOUR IP address (u can type it manually if you want)
ADDR = (SERVER,PORT)
FORMAT = "uft-8"
DISCONNECTED = "DISCONNECTED"

print("Host Name : " + socket.gethostname())  # Can be done by using direcly the public IPv4 of the host 
print("Host Address : "+ SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates TCP IPv4 Socket
server.bind(ADDR)        # Binds IP & PORT 


def client_mungling(connection,address):
    print(f"New connection : {address}")
    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)     # receiver the size (HEADER) the message must be & decodes it from binary to utf-8
        if msg_length:                                          # Checks if there is an actual message to send (if somebody has connected)
            msg_length = int(msg_length)                            # converts to int ( ObViOuSlY  (-_-) )
            message = connection.recv(msg_length).decode(FORMAT)    # actual message received with the proper length and decoded to uft-8
            if message == DISCONNECTED:                             # disconnects user (not to cause problems later)
                connected = False
            print(f"User [{address}] said : {message}")
            connection.send("Message received".encode(FORMAT))
    connection.close()                                          
    

"""
    Server listens for any connections until some connects:
        when some1 connects the server stores < server.accept() >:
            store their port & IP in < address > and the information about them (obj) in the < connection >
    !!!server.accept is a "blocker" : stays on same line until connection occurs!!!
        
"""
def start():
    server.listen()
    print(f"Server listening on : {SERVER}")
    while True:
        connection,address = server.accept() #Blocks & stocks conn and addr
        thread = threading.Thread(target=client_mungling, args=(connection,address)) # Creates & sends thread to client_mungling
        thread.start()

        print(f"Number of active connections : {threading.active_count() - 1}") # -1 because it has to exclude the host
print("Server is starting...")
start()

