import socket
import encodings.idna

PORT = 585
FORMAT = 'uft-8'
HEADER = 64
DISCONNECTED = "DISCONNECTED"
SERVER = "192.168.190.1"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def sendMessage(msg):
    message = msg.encode(FORMAT)    # Encodes the message (str) into BYTES format to send it to socket
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length)) # Cuz we need to make the message 64 bytes (header) we need to take the actual message length and substract it from the HEADER (64bytes) 
    #After subtracting the length of the message from the length of the header, we need to padd it: to make it 64 byes (b" "  = bytes "space" = adds emptry strings (spaces) to make the msg 64bytes)
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))



sendMessage("Surprise")
input()
sendMessage("mother fucker!")

sendMessage(DISCONNECTED)