from socket import *
import camera
import string
import os

SOCKET_PATH = "/tmp/pi_socket"  #server path

def connect_unix():
    if not os.path.exists(SOCKET_PATH):
        print("Socket not found")
        return

    # create the client socket (unix domain)
    clientsock = socket(AF_UNIX, SOCK_STREAM)

    # connect to the server socket file
    clientsock.connect(SOCKET_PATH)
    print("connected to C server!")

    while True:
        # read 1 byte from server (since C sends single char)
        data = clientsock.recv(1)
        if not data:
            break
        print("received:", data.decode())

    clientsock.close()
    print("client closed")

#call the function if run directly
if __name__ == "__main__":
    camera = camera.Camera()
    connect_unix()