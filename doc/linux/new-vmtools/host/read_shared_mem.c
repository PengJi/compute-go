#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define PAGE_SIZE 4096

int main() {
    int fd = open("/dev/my_shared_mem", O_RDWR);
    if (fd < 0) {
        perror("Failed to open the device");
        return -1;
    }

    char *shared_mem = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (shared_mem == MAP_FAILED) {
        perror("Failed to mmap");
        close(fd);
        return -1;
    }

    printf("Data from kernel: %s\n", shared_mem);

    munmap(shared_mem, PAGE_SIZE);
    close(fd);
    return 0;
}
