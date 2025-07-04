#include "client_socket.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    InitializeSocket();
    char input_buffer[16];
    char read_buffer[16];

    while(1) {
        printf("Enter a command: ");
        scanf("%s", input_buffer);

        if (strcmp(input_buffer, "record") == 0) {
            printf("Camera started recording\n");
            WriteToSocket("record");
            
            do {
                ReadFromSocket(read_buffer);
            } while (strcmp(read_buffer, "success") != 0);

            printf("Camera stopped recording\n");
        }

        if (strcmp(input_buffer, "quit") == 0) {
            printf("Exitting...");
            break;
        }
    }

    CloseSocket();
    return 0;

}