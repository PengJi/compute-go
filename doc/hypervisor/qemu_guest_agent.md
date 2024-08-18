# qemu-ga 介绍
# 使用
添加设备的 controller 
```xml
<controller type='virtio-serial' index='0' ports='2'>
  <alias name='virtio-serial0'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0'/>
</controller>
```

添加串口设备
```xml
<channel type='unix'>
  <source mode='bind' path='/var/lib/libvirt/qemu/channel/target/domain-2-abc1f073-d7e6-4f0d-9/org.qemu.guest_agent.0'/>
  <target type='virtio' name='org.qemu.guest_agent.0'/>
  <alias name='channel0'/>
  <address type='virtio-serial' controller='0' bus='0' port='1'/>
</channel>
```

上述 xml 转化为 qemu 参数如下：
```sh
-device virtio-serial-pci,id=virtio-serial0,max_ports=2,bus=pci.0,addr=0x8 
-chardev socket,id=charchannel0,fd=51,server,nowait 
-device virtserialport,bus=virtio-serial0.0,nr=1,chardev=charchannel0,id=channel0,name=org.qemu.guest_agent.0 
```
各参数含义如下：  
`-device virtio-serial-pci`  
创建一个 `virtio-serial` 的 PCI 代理设备，其初始化时会创建一条 `virtio-serial-bus`，用来挂载 `virtioserialport` 设备。

`-chardev socket`  
指定了一个字符设备，其后端设备对应为 `unix socket`，名字为 `virio-serial0`，在宿主机中可以看到类似于 `/var/lib/libvirt/qemu/channel/target/domain-42-fea480aa-5e8d-4eda-8/org.qemu.guest_agent.0` 的 socket 文件。

`-device virtserialport`  
创建一个 `virioserialport` 设备，其对应的 chardev 是 `virio-serial0`，名字是 `org.qemu_agent.0`，该设备会挂到 `virio-serial-bus` 上面，在虚拟机中我们就可以看到 `/dev/virtio-ports/org.qemu.guest_agent.0` 设备。

qemu 创建好了上述的设备之后，在虚拟机中执行 `qemu-ga --method=virtio-serial --path=/dev/virtio-ports/org.qemu.guest_agent.0`，就可以连接 `/dev/virtio-ports/org.qemu.guest_agent.0` 串口设备。在宿主机端可以连接 `/var/lib/libvirt/qemu/channel/target/domain-42-fea480aa-5e8d-4eda-8/org.qemu.guest_agent.0` 这个 `unix socket`，从而与虚拟机内部的 qemu-ga 通信，比如在宿主机端执行 guest-ping，虚拟机端的 qemu-ga 就返回执行结果。

# 通信
## 示例一
[使用virtio-serial实现guest OS与host的高效通信](https://blackskygg.github.io/2016/08/17/virtio-host-guest-communication/)  
添加 channel
```xml
<channel type='unix'>
    <source mode='bind' path='/home/ubuntu/vms/vm.ctl'/>
    <target type='virtio' address='virtio-serial' port='0'/>
</channel>
```
guest
```cpp
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
     int fd0;
     char *greetings = "Hi there!\n";

     fd0 = open("/dev/vport0p1", O_RDWR);
     for(;;) {
         write(fd0, greetings, strlen(greetings) + 1);
         sleep(1);  //一秒写一次
     }

     return 0;
}
```

host
```cpp
#include <unistd.h>
#include <sys/types.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    int sock;
    struct sockaddr_un addr;      // AF_UNIX的地址结构是sockaddr_un
    char buffer[512];

    sock = socket(AF_UNIX, SOCK_STREAM, 0);  //创建一个 UNIX domain socket
    addr.sun_family = AF_UNIX;
    strcpy(addr.sun_path, "vm.ctl");

    if(-1 == connect(sock, (struct sockaddr *)&addr, sizeof(addr)))
        perror("aha:");

    while(read(sock, buffer, 512)) {
        printf("data: %s\n", buffer);
        getchar();
    }

    return 0;
}
```

## 示例二
[基于virtio-serial的虚拟机和主机数据传输机制](https://blog.csdn.net/yzy1103203312/article/details/81661450)  
添加 channel
```xml
<channel type='unix'>
    <source mode='bind' path='/var/lib/libvirt/qemu/vm.data'/>
    <target type='virtio' address='virtio-serial' port='2'/>
</channel>
```

guest
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
 
#define CONTROL_PORT "/dev/vport0p2"
 
int main(void) {
	int fd;
	char * buf= "Test";
	int len, ret;
	
	fd = open(CONTROL_PORT, O_RDWR);
	if (fd == -1) {
		fprintf(stderr, "can't open vport\n");
		return -1;
	}
	
	ret = write(fd, buf, sizeof(buf));
		if (ret == -1) {
			fprintf(stderr, "can't write data to vport\n");
			return -1;
		}
	
	ret = close(CONTROL_PORT);
	if (ret < 0) {
		fprintf(stderr, "can't close vport\n");
		return -1;
	}
 
	return 0;
} 
```

host
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/un.h>
#include <sys/socket.h>
 
#define PORT "/var/lib/libvirt/qemu/vm.data"
 
int main(void) {
	int sock_fd;
	struct sockaddr_un sock;
	char buf[128];
	int ret;
 
	sock_fd = socket(AF_UNIX, SOCK_STREAM, 0);
	if ( sock_fd == -1 ) {
		fprintf(stderr, "Error: Socket can not be created !! \n");
        fprintf(stderr, "errno : %d\n", errno);
		return -1;
	}
 
	sock.sun_family = AF_UNIX;
	memcpy(&sock.sun_path, PORT, sizeof(sock.sun_path));
	ret = connect(sock_fd, (struct sockaddr *)&sock, sizeof(sock));
	if ( ret == -1) {
		fprintf(stderr, "Connect Failed!\n");
		return -1;
	}
	
	read(sock_fd, buf, 128);
	printf("%s\n",buf);
 
	close(sock_fd);
 
	
	return 0;
}
```

[Features/VirtioSerial](https://fedoraproject.org/wiki/Features/VirtioSerial)  
[交叉编译调试qemu_guest_agent](https://www.cnblogs.com/silvermagic/p/7666143.html)  
