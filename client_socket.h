#ifndef SOCKET_CLIENT_H
#define SOCKET_CLIENT_H

#define SOCKET_PATH "/tmp/pi_socket"

void InitializeSocket(void);
void ReadFromSocket(char* buffer);
void WriteToSocket(const char* message);
void CloseSocket(void);

#endif