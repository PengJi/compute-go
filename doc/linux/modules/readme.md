# host(4.19.90-2307.3.0.oe1.smartx.33.x86_64)
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

编译kvm
```bash
cd /usr/src/linux-4.19.90-2204.4.0.0146.oe1.x86_64
cp /boo/config-4.19.90-2204.4.0.0146.oe1.x86_64 /usr/src/linux-4.19.90-2204.4.0.0146.oe1.x86_64/.config
make olddefconfig
make -j$(nproc) -> compile.log
make modules SUBDIRS=arch/x86/kvm

# 卸载旧版本模块
modprobe -r kvm_intel && modprobe -r kvm

# 安装新版本模块
modprobe irqbypass && insmod kvm.ko && insmod kvm-intel.ko
```

# guest(openeuler-20.03 LTS SP4)
编译模块
```bash
make all
```

安装模块
```bash
insmod gpt_dump.ko
```

通过 dmesg 查看设备 major 
创建设备文件
```bash
mknod /dev/exampledev c {major} 0
```

编译应用程序
```bash
gcc guest_user.c
./a.out
```

# 卸载模块
```bash
rmmod gpt_dump.ko
```
