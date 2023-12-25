制作根文件系统
1. 编译 busybox
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
完成之后会在编译目录下生成 _install 目录（包含：`bin、linuxrc、sbin、usr`），主要包含一些可执行文件，此后需要将这些文件方的放到 rootfs。

2. 制作 rootfs
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

制作根文件系统镜像文件 rootfs.ext4，并将文件拷贝到 rootfs 目录
```bash
cp -r _install/ /hoem/jipeng/linux-build/rootfs_files
cd linux-build
mkdir rootfs
dd if=/dev/zero of=rootfs.ext4 bs=1M count=32
mkfs.ext4 rootfs.ext4
sudo mount -o loop rootfs.ext4 rootfs
sudo cp -rf rootfs_files/* rootfs
```

[从源码编译linux-4.9内核并运行一个最小的busybox文件系统](https://www.bilibili.com/read/cv11271232/)
