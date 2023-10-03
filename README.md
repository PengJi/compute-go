Build a hypervisor based on KVM with Rust

目标：
轻量低噪、软硬协同、安全

应用场景
特新需求
轻快灵活

[Using the KVM API](https://lwn.net/Articles/658511/)  


### 
kvmtools
StratoVrit
cloud-hypervisor
firecracker
kata-containers
microvm in qemu

# 运行
## 准备 Linux 内核镜像
```bash
wget https://repo.openeuler.org/openEuler-22.03-LTS/stratovirt_img/x86_64/vmlinux.bin
```

## 准备 initrd 文件系统镜像
### 下载 busybox
```bash
wget https://busybox.net/downloads/busybox-1.36.1.tar.bz2
tar -xjf busybox-1.36.1.tar.bz2
```

### 编译 busybox
```bash
cd busybox-1.36.1
make defconfig
make menuconfig
```
配置
```bash
Settings  --->
    [*] Build static binary (no shared libs)
```

### 安装 busybox
```bash
make install
```
在当前目录下会生成一个 _install 目录，里面包含了 busybox 的可执行文件和一些必要的文件。

### 配置 busybox
```bash
cd _install
mkdir proc sys dev etc etc/init.d
touch etc/init.d/rcS

cat >etc/init.d/rcS<<EOF
#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
/sbin/mdev -s
EOF

chmod +x etc/init.d/rcS
```

### 制作 ininrd 镜像
```bash
cd _install
find . | cpio -o --format=newc > /tmp/StratoVirt-initrd
```

### 生成 hypervisor
```bash
cargo build --release
```

### 运行
```bash
./target/release/stratovirt \
    -machine microvm \
    -kernel ./vmlinux.bin \
    -append "console=ttyS0 reboot=k panic=1 root=/dev/ram rdinit=/bin/sh" \
    -initrd /tmp/StratoVirt-initrd \
    -qmp unix:./qmp.sock,server,nowait \
    -serial stdio
```