在用户空间直接写 nvme 裸盘示例

准备环境
`/dev/nvme1n1` 是一个 nvme 裸盘，没有分区，没有文件系统

```bash
sudo dd if=/dev/zero of=/dev/nvme1n1  # 写一会 ctrl+c 中断
# 确认盘上数据全是 0
sudo cat /dev/nvme1n1  # 正常无输出
```

编写程序（nvme.c）
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <linux/nvme_ioctl.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

int main() {
    int fd = open("/dev/nvme1n1", O_RDWR);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    char *buffer = malloc(4096);
    if (!buffer) {
        perror("malloc");
        return 1;
    }

    memset(buffer, 0, 4096);

    struct nvme_user_io io;
    io.addr = (__u64) buffer;
    io.slba = 0;
    io.nblocks = 1;
    io.opcode = 1; // write

    strcpy(buffer, "Hello, world!");

    if(ioctl(fd, NVME_IOCTL_SUBMIT_IO, &io) == -1) {
        perror("failed to submit write io request\n");
        close(fd);
        free(buffer);
        return 1;
    }

    printf("write success\n");

    memset(buffer, 0, 4096);
    io.addr = (__u64) buffer;
    io.slba = 0;
    io.nblocks = 1;
    io.opcode = 2; // read

    if(ioctl(fd, NVME_IOCTL_SUBMIT_IO, &io) == -1) {
        perror("failed to submit read io request\n");
        close(fd);
        free(buffer);
        return 1;
    }

    printf("read success\n");
    printf("read data: %s\n", buffer);
    close(fd);
    free(buffer);

    return 0;
    
}
```

在 `linux-5.15` 上编译运行
```bash
gcc nvme.c -o nvme
./nvme

write success
read success
read data: Hello, world!

sudo cat /dev/nvme1n1

Hello, world!
```
