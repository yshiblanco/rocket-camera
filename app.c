#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>

#define SOCKET_PATH "/tmp/pi_socket"
#define SOCKET_TYPE SOCK_STREAM
#define DOMAIN      AF_UNIX

int main(void) {
    int serverSocket;
    int clientSocket;
    struct sockaddr_un serverAddr;
    struct sockaddr_un clientAddr;
    int ret;                                //For errors
    //Remove existing socket file if it exists
    unlink(SOCKET_PATH);
    //Creating socket
    serverSocket = socket(DOMAIN, SOCKET_TYPE, 0);
    //Assigning an address to the socket
    serverAddr.sun_family = DOMAIN;
    strcpy(serverAddr.sun_path, SOCKET_PATH);
    int serverAddrLen = sizeof(serverAddr);
    ret = bind(serverSocket, (struct sockaddr* ) &serverAddr, serverAddrLen);
    if (ret == -1) {
        printf("Failure with bind() call\n");
        return 1;
    }
    //Listen for incoming connection requests (max of 1 in connection queue)
    ret = listen(serverSocket, 1);
    if (ret == -1) {
        printf("Failure with listen() call\n");
        return 1;
    }
    //Wait for a connection from a client
    printf("Waiting for connection...\n");
    socklen_t clientAddrLen = sizeof(clientAddr);
    clientSocket = accept(serverSocket, (struct sockaddr* ) &clientAddr, &clientAddrLen);
    if (clientSocket == -1) {
        printf("Failure with accept() call\n");
        return 1;
    }
    printf("Connected to client\n");
    while(1) {
        char ch = 'H';
        ssize_t bytesWritten = write(clientSocket, &ch, sizeof(ch));
        if (bytesWritten <= 0) {
            printf("Failure with write() call\n");
            close(clientSocket);
            close(serverSocket);
            return 1;
        }
        sleep(5);
    }
    return 0;
}