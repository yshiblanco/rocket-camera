#include "client_socket.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>

#define SOCKET_TYPE SOCK_STREAM
#define DOMAIN AF_UNIX

int client_socket;
struct sockaddr_un client_addr;

void InitializeSocket(void) {
    /* @brief Opens communication to the server side of the socket */

    //Creating socket
    client_socket = socket(DOMAIN, SOCKET_TYPE, 0);

    //Assigning an address to the socket
    client_addr.sun_family = DOMAIN;
    strcpy(client_addr.sun_path, SOCKET_PATH);

    //Connecting to the server socket
    connect(client_socket, (struct sockaddr *) &client_addr, sizeof(client_addr));

}

void ReadFromSocket(char* buffer) {
    /*
    * @brief Reads the first 15 characters sent over the socket
    *
    * @param buffer: Stores read string, should be at least 16 bytes long
    */

    ssize_t bytes_read = read(client_socket, buffer, 15);
    buffer[bytes_read] = '\0';

}

void WriteToSocket(const char* message) {
    /*
    * @brief Sends message over the socket to the server
    *
    * @param message: String to be sent
    */
    write(client_socket, message, strlen(message));
}

void CloseSocket(void) {
    /* Closes the socket connection */
    close(client_socket);
}