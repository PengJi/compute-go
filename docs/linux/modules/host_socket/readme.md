编译监听模块
```bash
make all
```

安装模块
```bash
insmod kernel_socket.ko
```

监听 socket
```bash
gcc user_socket_listener.c
./a.out
```
