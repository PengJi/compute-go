#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main() {
    int fd;
    char read_buf[100];
    char write_buf[] = "Hello, device!";

    fd = open("/dev/exampledev", O_RDWR);
    if (fd < 0) {
        perror("Failed to open the device");
        return -1;
    }

    write(fd, write_buf, strlen(write_buf));
    read(fd, read_buf, sizeof(read_buf));
    printf("Received from device: %s\n", read_buf);

    close(fd);
    return 0;
}
