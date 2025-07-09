#include <sys/un.h>

#define SOCKET_PATH "/tmp/pi_socket"
#define SOCKET_TYPE "SOCK_STREAM"
#define DOMAIN      "AF_UNIX"
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
