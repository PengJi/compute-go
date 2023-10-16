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

## 编译 linux
参照 linux.md 的步骤，配置内核，主要是开启 virtio 相关的模块。
```sh
 - For the default console output:
	CONFIG_SERIAL_8250=y
	CONFIG_SERIAL_8250_CONSOLE=y

 - For running 32bit images on 64bit hosts:
	CONFIG_IA32_EMULATION=y

 - Proper FS options according to image FS (e.g. CONFIG_EXT2_FS, CONFIG_EXT4_FS).

 - For all virtio devices listed below:
	CONFIG_VIRTIO=y
	CONFIG_VIRTIO_RING=y
	CONFIG_VIRTIO_PCI=y

 - For virtio-blk devices (--disk, -d):
	CONFIG_VIRTIO_BLK=y

 - For virtio-net devices ([--network, -n] virtio):
	CONFIG_VIRTIO_NET=y

 - For virtio-9p devices (--virtio-9p):
	CONFIG_NET_9P=y
	CONFIG_NET_9P_VIRTIO=y
	CONFIG_9P_FS=y

 - For virtio-balloon device (--balloon):
	CONFIG_VIRTIO_BALLOON=y

 - For virtio-console device (--console virtio):
	CONFIG_VIRTIO_CONSOLE=y

 - For virtio-rng device (--rng):
	CONFIG_HW_RANDOM_VIRTIO=y

 - For vesa device (--sdl or --vnc):
	CONFIG_FB_VESA=y

# 需默认开启的模块
# https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/about/

```
编译内核完成之后在 `/arch/x86/boot/` 目录下生成 `bzImage` 文件。


## 制作根文件系统
busybox 是一个集成了多个最常用 linux 命令和工具的软件，可以用来制作根文件系统。
```sh
wget https://busybox.net/downloads/busybox-1.36.1.tar.bz2
tar -xvf busybox-1.36.1.tar.bz2
cd busybox-1.36.1/
make menuconfig
# 配置为静态编译
-> Settings
  -> Build Options
    -> Build BusyBox as a static binary (no shared libs)

# 编译并安装
make -j$(nproc)
make install
```
完成之后会在编译目录下生成 _install 目录（包含：`bin/linuxrc/sbin/usr`），主要包含一些可执行文件，此后需要将这些文件方的放到 rootfs。

制作 rootfs
```sh
# rootfs 目录中新建 linux 根目录树
cd busybox-1.36.1/_install/
sudo mkdir  dev  etc  lib  var  proc  tmp  home  root  mnt  sys
# 各目录说明如下:
# /dev: 存储特殊文件或设备文件
# /etc: 系统配置文件
# /home: 普通用户目录
# /lib: 为系统启动或根文件上的应用程序（/bin,/sbin等）提供共享库，以及为内核提供内核模块
# /bin: 系统管理员和用户均可使用的命令
# /sbin： 系统管理员使用的系统命令
# /root：root用户目录
# /mnt：临时挂载点
# /proc: 基于内存的虚拟文件系统，用于为内核及进程存储其相关信息
# /sys：sysfs虚拟文件系统提供了一种比proc更为理想的访问内核数据的途径：其主要作用在于为管理linux设备提供一种统一模型的接口；
# /usr：usr hierarchy，全局共享的只读数据路径
# /var：存储常发生变化的数据目录：cache、log等
# /tmp: 临时文件存储目录
```

创建根目录所必需的文件
注：也可拷贝 busybox 的配置目录，包含：fstab/init.d/inittab/profile
`sudo cp busybox-1.36.1/examples/bootfloppy/etc/*  rootfs/etc -r`

```sh
# 修改 fstab
cd _install/
cat> etc/fstab << EOF
proc  /proc proc  defaults 0 0
tmpfs  /tmp  tmpfs  defaults 0 0
none  /tmp  ramfs defaults 0 0
sysfs /sys  sysfs defaults 0 0
mdev  /dev  ramfs defaults 0 0
EOF

# 修改 profile
cd _install/
cat> etc/profile << EOF
# /etc/profile: system-wide .profile file for the Bourne shells

PATH=/bin:/sbin:/usr/bin:/usr/sbin #可执行程序 环境变量
export LD_LIBRARY_PATH=/lib:/usr/lib #动态链接库 环境变量
/bin/hostname kvmtool-test
USER="`id -un`"
LOGNAME=$USER
HOSTNAME='/bin/hostname'
PS1='[\u@\h \W]# ' #显示主机名、当前路径等信息
EOF

# 修改 initab
cd _install/
cat > etc/inittab << EOF
::sysinit:/etc/init.d/rcS
tty0::askfirst:-/bin/sh
::respawn:-/bin/sh
::askfirst:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
EOF
chmod 755 etc/inittab

# 修改 rcS
cd _install/
cat > etc/init.d/rcS << EOF
/bin/mount -a
mkdir -p /dev/pts
mount -t devpts devpts /dev/pts
echo /sbin/mdev > /proc/sys/kernel/hotplug
mdev -s
echo "************Welcome to mini Linux************"
EOF
chmod 755 etc/init.d/rcS

# 添加设备文件
cd _install/dev
sudo mknod console c 5 1
sudo mknod null c 1 3
sudo mknod tty1 c 4 1
cd -
```

制作根文件系统镜像文件 rootfs.cpio.gz
```bash
cd _install
find . | cpio -o -H newc > ../rootfs.cpio
cd ..
gzip -c rootfs.cpio > rootfs.cpio.gz
```

制作根文件系统镜像文件 rootfs.ext4
```bash
cd busybox-1.36.1
dd if=/dev/zero of=rootfs.ext4 bs=1M count=32
mkfs.ext4 rootfs.ext4
mkdir -p rootfs
sudo mount -o loop rootfs.ext4 rootfs
sudo cp -rf _install/* rootfs
```

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

基于disk启动方式
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
