#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define device_name "/dev/guestping"

int main() {
    int fd;
    char read_buf[100];
    char write_buf[] = "message from userspace!";

    fd = open(device_name, O_RDWR);
    if (fd < 0) {
        perror("Failed to open the device");
        return -1;
    }

    write(fd, write_buf, strlen(write_buf));
    printf("message sent\n");
    // read(fd, read_buf, sizeof(read_buf));
    // printf("Received from device: %s\n", read_buf);

    close(fd);
    return 0;
}
