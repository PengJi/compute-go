#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <sys/select.h>

#define DATA_NUM    (64)

int main(int argc, char *argv[])
{
    int fd, i;
    int r_len, w_len;
    fd_set fdset;
    char buf[DATA_NUM] = "hello world";

    memset(buf, 0, DATA_NUM);

    // 打开设备文件
    // 当调用 open 函数时，将会调用驱动中的 hello_open
    fd = open("/dev/helloworld", O_RDWR);
	printf("%d\r\n",fd);
    if(fd == -1) {
      	perror("open file error\r\n");
		return -1;
    } else {
		printf("open successe\r\n");
	}
    
    // 将会调用驱动中的 hello_write，其返回值为 hello_write 的返回值
    w_len = write(fd, buf, DATA_NUM);

    // 将会调用驱动中的 hello_read，其返回值为 hello_read 的返回值
    r_len = read(fd, buf, DATA_NUM);

    printf("%d %d\r\n", w_len, r_len);
    printf("%s\r\n", buf);

    // 注意此处没有 close

    return 0;
}
