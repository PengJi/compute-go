# [kvmtool](https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/)

# 安装使用
## 编译 kvmtool
```sh
git clone git://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git
cd kvmtool
make -j$(nproc)
# 将生成的 kvmtool 可执行文件拷贝到 /usr/local/bin
sudo cp lkvm /usr/local/bin
```

## 制作根文件系统
参考 [linux/rootfs.md](linux/rootfs.md)

## 启动虚拟机
基于 initrd 启动方式
```bash
lkvm run \
--kernel linux-4.19/arch/x86/boot/bzImage \
--initrd busybox-1.36.1/rootfs.cpio.gz \
--param "root=/dev/ram rdinit=/linuxrc" \
--console serial  \
--name vm1
```

基于 disk 启动方式
```bash
lkvm run \
--kernel linux-4.19/arch/x86/boot/bzImage \
--disk busybox-1.36.1/rootfs.ext4 \
--console serial \
--name vm1
```


```sh
lkvm run \
--kernel linux-4.19/arch/x86/boot/bzImage \
--disk rootfs.img \
--network virtio \
--console serial \
--name vm1

成功启动后提示
```bash
[    0.736470] Run /sbin/init as init process
************Welcome to mini Linux************

```

## 进入 guest OS 配置网络
```sh
ip link list
ip link set eth0 up
ip addr add 192.168.33.100/24 dev eth0
ip a
```

[kvmtool - a QEMU alternative?](https://elinux.org/images/4/44/Przywara.pdf)  
