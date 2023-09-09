# 编译安装
```sh
# 安装编译所需的依赖包
sudo apt install autoconf automake autotools-dev curl \
    libmpc-dev libmpfr-dev libgmp-dev \
    gawk build-essential bison flex texinfo gperf libtool patchutils bc \
    zlib1g-dev libexpat-dev pkg-config libglib2.0-dev libpixman-1-dev libsdl2-dev \
    git tmux python3 python3-pip ninja-build

# 下载源码包
wget https://download.qemu.org/qemu-7.0.0.tar.xz

# 解压
tar xvJf qemu-7.0.0.tar.xz

# 编译安装并配置 RISC-V 支持
cd qemu-7.0.0
./configure \
--target-list=riscv64-softmmu,riscv64-linux-user,x86_64-softmmu,x86_64-linux-user \
--enable-sdl  # 支持图形界面
# Install prefix               : /usr/local
# BIOS directory               : share/qemu
# firmware path                : /usr/local/share/qemu-firmware
# binary directory             : bin
# library directory            : lib
# module directory             : lib/qemu
# libexec directory            : libexec
# include directory            : include
# config directory             : /usr/local/etc
# local state directory        : /usr/local/var
# Manual directory             : share/man
# Doc directory                : /usr/local/share/doc
# Build directory              : /home/jipeng/app/qemu-7.0.0/build
# Source path                  : /home/jipeng/app/qemu-7.0.0
# GIT submodules               : ui/keycodemapdb tests/fp/berkeley-testfloat-3 tests/fp/berkeley-softfloat-3 dtc capstone slirp


# 编译
make -j$(nproc)

# 安装
sudo make install
# 这种方式可能与安装的其他版本冲突，另外一种更灵活的做法是将编译生成二进制文件的路径添加到 PATH 环境变量中，例如：
vi /etc/profile
export PATH=$PATH:/path/to/qemu-7.0.0/build
source /etc/profile

# 确认安装的版本
qemu-system-riscv64 --version
qemu-riscv64 --version
qemu-system-x86_64 --version
qemu-x86_64 --version
```

# 使用 qemu
## 快捷键（chardev/char-mux.c）
退出 qemu
`ctrl+a x`

查看配置
`ctrl+a c`
info registers

待探索
`ctrl+a h`
`ctrl+a s`
`ctrl+a b`
`ctrl+a t`

## 常用命令行
```bash
# 查看支持的设备
qemu-system-x86_64 -device help
```

## 使用 qemu
### 配置参数详解
配置 CPU
```bash

```

### 安装 guest OS 
创建 qcow2 磁盘
```bash
qemu-img create -f qcow2 centos-7_9.img 20G
```

启动 guest OS
centos7.9 version 3.10
```sh
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 4,maxcpus=32,sockets=16,cores=2,threads=1 \
-m size=4G,slots=255,maxmem=8G \
-device piix3-usb-uhci,id=usb,bus=pci.0,addr=0x1.0x2 \
-device nec-usb-xhci,p2=15,p3=15,id=usb1,bus=pci.0,addr=0x5 \
-device usb-ehci,id=usb2,bus=pci.0,addr=0x6 \
-device piix3-usb-uhci,id=usb3,bus=pci.0,addr=0x7 \
-drive if=none,format=qcow2,file=/home/jipeng/centos-7_9.img,id=disk0 \
-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=disk0,id=virtio-disk0,bootindex=1,write-cache=on \
-drive file=/home/jipeng/Downloads/CentOS-7-x86_64-DVD-2009.iso,file.locking=off,format=raw,if=none,id=drive-ide0-0-0,readonly=on \
-device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=2 \
-vnc :0 \
-monitor stdio \
-chardev socket,id=qmp,port=4444,host=localhost,server=on \
-mon chardev=qmp,mode=control,pretty=on
```

openEuler 22.03 version 5.10
```sh
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 4,maxcpus=32,sockets=16,cores=2,threads=1 \
-m size=4G,slots=255,maxmem=8G \
-device piix3-usb-uhci,id=usb,bus=pci.0,addr=0x1.0x2 \
-device nec-usb-xhci,p2=15,p3=15,id=usb1,bus=pci.0,addr=0x5 \
-device usb-ehci,id=usb2,bus=pci.0,addr=0x6 \
-device piix3-usb-uhci,id=usb3,bus=pci.0,addr=0x7 \
-drive if=none,format=qcow2,file=/home/jipeng/openEuler-22_03.img,id=disk0 \
-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=disk0,id=virtio-disk0,bootindex=1,write-cache=on \
-drive file=/home/jipeng/Downloads/openEuler-22.03-LTS-x86_64-dvd.iso,file.locking=off,format=raw,if=none,id=drive-ide0-0-0,readonly=on \
-device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=2 \
-vnc :1 \
-monitor stdio 
```

指定 vnc 地址和端口，可使用 vnc viewer 连接，比如：192.168.74.83:5
`-vnc 192.168.74.83:5`
连接时的地址为 192.168.74.83:5905

在启动 qemu 之后，进入交互式命令行，之后可执行 hmp 命令
`-monitor stdio`   

通过 tcp 与 qemu 交互，可执行 qmp 命令
```bash
-chardev socket,id=qmp,port=4444,host=localhost,server \
-mon chardev=qmp,mode=control,pretty=on
```

添加 cdrom
```bash
-drive file=/usr/share/smartx/images/ae5d0ad2-ee8b-4be8-a5e9-dd55f8beee62,file.locking=off,format=raw,if=none,id=drive-ide0-0-0,readonly=on \
-device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=2
```

添加 virtio-blk
```bash
-drive file.driver=iscsi,file.portal=127.0.0.1:3260,file.target=iqn.2016-02.com.smartx:system:zbs-iscsi-datastore-1637755567369y,file.lun=127,file.transport=tcp,format=raw,if=none,id=drive-virtio-disk0,cache=none,aio=native \
-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=drive-virtio-disk0,id=virtio-disk0,bootindex=1,write-cache=on \
```

## 连接 qemu monitor
有多种方式可以连接 qemu monitor，连接后可以通过 qmp 协议与 qemu 交互。

### 通过标准输入/输出执行 qmp
建立 qmp 连接
```bash
-chardev stdio,id=mon0 \
-mon chardev=mon0,mode=control,pretty=on
```
连接后首先会进入协商模式，退出协商模式
```bash
{"execute": "qmp_capabilities"}
```
之后进入命令模式，注意：窗口中也会输出所有 qmp 事件
```bash
# 弹出 cdrom
{"execute": "eject", "arguments": {"device": "ide1-cd0"}}

# 查询时间
{"execute": "query-events"}
```

### 通过套接字执行 qmp
qemu monitor 采用 tcp 方式 ，监听在 127.0.0.1 上，端口为 4444。
```bash
-chardev socket,id=mon0,host=localhost,port=4444,server,nowait \
-mon chardev=mon0,mode=control,pretty=on
```
或者
```bash
-qmp tcp:127.0.0.1:4444,server,nowait
```

可以创建多个 qemu monitor。
```bash
-chardev stdio,id=mon0 \
-mon chardev=mon0,mode=readline \
-chardev socket,id=mon1,host=localhost,port=4444,server,nowait \
-mon chardev=mon1,mode=control,pretty=on
```

运行 telnet 连接 qemu monitor
```bash
telnet localhost 4444
Trying ::1...
Connected to localhost.
Escape character is '^]'.
{
    "QMP": {
        "version": {
            "qemu": {
                "micro": 0,
                "minor": 0,
                "major": 2
            },
            "package": ""
        },
        "capabilities": [
        ]
    }
}
```

### 通过 unix socket 执行 qmp
qemu monitor 采用 unix socket，socket 文件生成于/tmp/qmp.socket
```bash
-qmp unix:/tmp/qmp.socket,server,nowait
```

通过 /tmp/qmp.socket 套接字来与 QEMU 通信，打开另一个终端中使用 nc
```bash
sudo nc -U /tmp/qmp.socket
{"QMP": {"version": {"qemu": {"micro": 0, "minor": 0, "major": 2} [...]
```

### qmp 示例
```bash
# 查看支持哪些qmp指令
{"execute": "query-commands"}

# 虚拟机状态
{"execute": "query-status"}

# 虚拟机暂停
{"execute": "stop"}

# 磁盘查看
{"execute": "query-block"}

# 磁盘在线插入
{"execute": "blockdev-add", "arguments": {"driver": "qcow2", "node-name": "drive-virtio-disk1", "file": {"driver": "file", "filename": "/opt/data.qcow2"}}}
{"execute": "device_add", "arguments": {"driver": "virtio-blk-pci", "drive": "drive-virtio-disk1"}}

# 磁盘完整备份
{"execute" : "drive-backup" , "arguments" : {"device" : "drive-virtio-disk0" , "sync" : "full" , "target" : "/opt/backuptest/fullbackup.img"}}
```

[QEMU QMP Reference Manual](https://qemu.readthedocs.io/en/latest/interop/qemu-qmp-ref.html)

### 使用 hmp
hmp 简化了 qmp，可以通过 monitor stdio 进入 hmp 命令行，也可以通过 qmp 进入 hmp 命令行，其底层仍然使用 qmp 协议。
参数
```bash
-monitor stdio
```
使用上述参数启动 qemu，会出现交互界面。
示例
```bash
# 查看支持的命令
(qemu) help

# 直接输入 info 回车，可以看到所有查询类的指令使用方法
(qemu) info

# 查看块设备
(qemu) info block

# 在线增加磁盘
(qemu) drive_add 0 file=/opt/data.qcow2,format=qcow2,id=drive-virtio-disk1,if=none
(qemu) device_add virtio-blk-pci,scsi=off,drive=drive-virtio-disk1

# 热添加 cdrom
(qemu) device_add virtio-scsi-pci,id=scsi0
(qemu) drive_add 0 id=cdrom0,if=none,format=raw,readonly=on,file=/usr/share/test.iso
(qemu) device_add scsi-cd,bus=scsi0.0,drive=cdrom0

# 热添加 cdrom
(qemu) drive_add auto id=usb_cdrom_drive,if=none,file=/usr/share/test.iso,media=cdrom
(qemu) device_add usb-storage,id=usb_cdrom_device,drive=usb_cdrom_drive,bus=usb.0,port=2

# 深信服热添加 cdrom
(qemu) drive_add auto id=usb_cdrom_fastio_drive_id,if=none,file=/usr/share/test.iso,media=cdrom
(qemu) device_add usb-storage,id=usb_cdrom_fastio_device_id,drive=usb_cdrom_fastio_drive_id,bus=usb-bus.0,port=1.1
```

## 使用 qemu-guest-agent
命令行参数
```bash
-chardev socket,id=charmonitor,path=/var/lib/libvirt/qemu/domain-1-ubuntu20.04-agent.sock,server,nowait \
```

[QEMU Guest Agent Protocol Reference](https://qemu.readthedocs.io/en/latest/interop/qemu-ga-ref.html)
