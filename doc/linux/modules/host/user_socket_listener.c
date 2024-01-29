#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#define SOCKET_PATH "/tmp/kernel_socket"

int main() {
    int sock_fd, client_fd;
    struct sockaddr_un addr;
    char buffer[1024];
    ssize_t numRead;

    sock_fd = socket(AF_UNIX, SOCK_DGRAM, 0);
    if (sock_fd == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    memset(&addr, 0, sizeof(struct sockaddr_un));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

    // 确保地址不存在
    unlink(SOCKET_PATH);

    if (bind(sock_fd, (struct sockaddr *)&addr, sizeof(struct sockaddr_un)) == -1) {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    while (1) {
        numRead = recvfrom(sock_fd, buffer, sizeof(buffer), 0, NULL, NULL);
        if (numRead == -1) {
            perror("recvfrom");
            exit(EXIT_FAILURE);
        }
        
        printf("Received: %s\n", buffer);
    }

    close(sock_fd);
    return 0;
}
