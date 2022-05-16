import socket
import sys
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!Disconnect"
#ADDR IS A TUPLE WHICH IS USED IN server.bind
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Everything that connects to this address will hit this socket
server.bind(ADDR)



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            #conn.send("Msg received".encode(FORMAT))
    conn.close()

# handles initial connections and handles where that information is going
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}"  )
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=( conn, addr))
        thread.start()
        print(f"[Active connections] {threading.activeCount() - 1} ")

print("Serer is starting....")
start()