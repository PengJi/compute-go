# [QEMU](https://gitlab.com/qemu-project/qemu)

# 编译安装
```sh
# 安装编译所需的依赖包
sudo apt install autoconf automake autotools-dev curl \
    git tmux python3 python3-pip ninja-build meson pkg-config \
    gawk build-essential bison flex texinfo gperf libtool patchutils bc \
    libmpc-dev libmpfr-dev libgmp-dev \
    zlib1g-dev libexpat-dev libglib2.0-dev libpixman-1-dev \
    libsdl2-dev \
    libspice-server-dev libspice-protocol-dev \
    libnfs-dev liburing-dev \
    librdmacm-dev libibverbs-dev \
    librados-dev librbd-dev \
    libfuse-dev libfuse3-dev\
    libibumad-dev \
    libcap-ng-dev libattr1-dev libseccomp-dev

# 下载源码包
wget https://download.qemu.org/qemu-7.0.0.tar.xz

# 解压
tar xvJf qemu-7.0.0.tar.xz

# 编译安装并配置 RISC-V 支持，安装在特定位置
cd qemu-7.0.0
./configure \
--prefix=/usr \
--target-list=riscv64-softmmu,riscv64-linux-user,x86_64-softmmu,x86_64-linux-user \
--enable-sdl \
--enable-spice \
--enable-kvm \
--enable-rdma \
--enable-rbd \
--enable-fuse \
--enable-virtfs \
--enable-virtiofsd
# 上述 prefix 也可为： --prefix=$HOME/qemu_build \
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
# 文件位于 $HOME/qemu_build
vi /etc/profile
export PATH=$PATH:$HOME/qemu_build
source /etc/profile

# 确认安装的版本
qemu-system-riscv64 --version
qemu-riscv64 --version
qemu-system-x86_64 --version
qemu-x86_64 --version
```

上述将 qemu 安装在了 $HOME/qemu_build 目录下，如果要使用 libvirt，需要安装到 `/usr`，指定 `--prefix=/usr`，libvirt 也默认安装在 `/usr`

具体的安装位置：
```bash
Installing subprojects/dtc/libfdt/libfdt.a to /usr/lib/x86_64-linux-gnu
Installing trace/trace-events-all to /usr/share/qemu
Installing qemu-system-riscv64 to /usr/bin
Installing qemu-riscv64 to /usr/bin
Installing qemu-system-x86_64 to /usr/bin
Installing qemu-x86_64 to /usr/bin
Installing qga/qemu-ga to /usr/bin
Installing qemu-keymap to /usr/bin
Installing qemu-img to /usr/bin
Installing qemu-io to /usr/bin
Installing qemu-nbd to /usr/bin
Installing storage-daemon/qemu-storage-daemon to /usr/bin
Installing qemu-edid to /usr/bin
Installing qemu-bridge-helper to /usr/libexec
Installing qemu-pr-helper to /usr/bin
Installing pc-bios/edk2-aarch64-code.fd to /usr/share/qemu
Installing pc-bios/edk2-arm-code.fd to /usr/share/qemu
Installing pc-bios/edk2-arm-vars.fd to /usr/share/qemu
Installing pc-bios/edk2-i386-code.fd to /usr/share/qemu
Installing pc-bios/edk2-i386-secure-code.fd to /usr/share/qemu
Installing pc-bios/edk2-i386-vars.fd to /usr/share/qemu
Installing pc-bios/edk2-x86_64-code.fd to /usr/share/qemu
Installing pc-bios/edk2-x86_64-secure-code.fd to /usr/share/qemu
Installing pc-bios/keymaps/ar to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/bepo to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/cz to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/da to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/de to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/de-ch to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/en-gb to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/en-us to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/es to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/et to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/fi to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/fo to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/fr to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/fr-be to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/fr-ca to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/fr-ch to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/hr to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/hu to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/is to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/it to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/ja to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/lt to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/lv to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/mk to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/nl to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/no to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/pl to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/pt to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/pt-br to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/ru to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/th to /usr/share/qemu/keymaps
Installing pc-bios/keymaps/tr to /usr/share/qemu/keymaps
Installing /home/jipeng/qemu/subprojects/dtc/libfdt/fdt.h to /usr/include/
Installing /home/jipeng/qemu/subprojects/dtc/libfdt/libfdt.h to /usr/include/
Installing /home/jipeng/qemu/subprojects/dtc/libfdt/libfdt_env.h to /usr/include/
Installing /home/jipeng/qemu/include/qemu/qemu-plugin.h to /usr/include/
Installing new directory /var/run
Installing /home/jipeng/qemu/build/meson-private/libfdt.pc to /usr/lib/x86_64-linux-gnu/pkgconfig
Installing /home/jipeng/qemu/ui/icons/qemu_16x16.png to /usr/share/icons/hicolor/16x16/apps
Installing /home/jipeng/qemu/ui/icons/qemu_24x24.png to /usr/share/icons/hicolor/24x24/apps
Installing /home/jipeng/qemu/ui/icons/qemu_32x32.png to /usr/share/icons/hicolor/32x32/apps
Installing /home/jipeng/qemu/ui/icons/qemu_48x48.png to /usr/share/icons/hicolor/48x48/apps
Installing /home/jipeng/qemu/ui/icons/qemu_64x64.png to /usr/share/icons/hicolor/64x64/apps
Installing /home/jipeng/qemu/ui/icons/qemu_128x128.png to /usr/share/icons/hicolor/128x128/apps
Installing /home/jipeng/qemu/ui/icons/qemu_256x256.png to /usr/share/icons/hicolor/256x256/apps
Installing /home/jipeng/qemu/ui/icons/qemu_512x512.png to /usr/share/icons/hicolor/512x512/apps
Installing /home/jipeng/qemu/ui/icons/qemu_32x32.bmp to /usr/share/icons/hicolor/32x32/apps
Installing /home/jipeng/qemu/ui/icons/qemu.svg to /usr/share/icons/hicolor/scalable/apps
Installing /home/jipeng/qemu/ui/qemu.desktop to /usr/share/applications
Installing /home/jipeng/qemu/pc-bios/bios.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/bios-256k.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/bios-microvm.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/qboot.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-cirrus.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-stdvga.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-vmware.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-qxl.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-virtio.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-ramfb.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-bochs-display.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vgabios-ati.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/openbios-sparc32 to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/openbios-sparc64 to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/openbios-ppc to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/QEMU,tcx.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/QEMU,cgthree.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pxe-e1000.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pxe-eepro100.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pxe-ne2k_pci.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pxe-pcnet.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pxe-rtl8139.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pxe-virtio.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-e1000.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-eepro100.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-ne2k_pci.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-pcnet.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-rtl8139.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-virtio.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-e1000e.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/efi-vmxnet3.rom to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/qemu-nsis.bmp to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/multiboot.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/multiboot_dma.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/linuxboot.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/linuxboot_dma.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/kvmvapic.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/pvh.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/s390-ccw.img to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/s390-netboot.img to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/slof.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/skiboot.lid to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/palcode-clipper to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/u-boot.e500 to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/u-boot-sam460-20100605.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/qemu_vga.ndrv to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/edk2-licenses.txt to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/hppa-firmware.img to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/opensbi-riscv32-generic-fw_dynamic.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/opensbi-riscv64-generic-fw_dynamic.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/npcm7xx_bootrom.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vof.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/vof-nvram.bin to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/bamboo.dtb to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/canyonlands.dtb to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/petalogix-s3adsp1800.dtb to /usr/share/qemu
Installing /home/jipeng/qemu/pc-bios/petalogix-ml605.dtb to /usr/share/qemu
Installing /home/jipeng/qemu/build/pc-bios/descriptors/50-edk2-i386-secure.json to /usr/share/qemu/firmware
Installing /home/jipeng/qemu/build/pc-bios/descriptors/50-edk2-x86_64-secure.json to /usr/share/qemu/firmware
Installing /home/jipeng/qemu/build/pc-bios/descriptors/60-edk2-aarch64.json to /usr/share/qemu/firmware
Installing /home/jipeng/qemu/build/pc-bios/descriptors/60-edk2-arm.json to /usr/share/qemu/firmware
Installing /home/jipeng/qemu/build/pc-bios/descriptors/60-edk2-i386.json to /usr/share/qemu/firmware
Installing /home/jipeng/qemu/build/pc-bios/descriptors/60-edk2-x86_64.json to /usr/share/qemu/firmware
Installing /home/jipeng/qemu/pc-bios/keymaps/sl to /usr/share/qemu/keymaps
Installing /home/jipeng/qemu/pc-bios/keymaps/sv to /usr/share/qemu/keymaps
make[1]: Leaving directory '/home/jipeng/qemu/build
```

# 使用 qemu
## 快捷键（chardev/char-mux.c）
退出 qemu
`ctrl+a x`

查看配置
`ctrl+a c`
info registers

切换qemu控制台
`ctrl+alt+2`

切换回调试kernel
`ctrl+alt+1`

将被qemu VM捕获的鼠标焦点切换回host
`ctrl+alt`

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

## qemu debug
[Debugging early startup of KVM with GDB, when launched by libvirtd](https://www.berrange.com/posts/2011/10/12/debugging-early-startup-of-kvm-with-gdb-when-launched-by-libvirtd/)  

## 安装 guest OS 
### 创建 qcow2 磁盘
```bash
qemu-img create -f qcow2 centos-7_9.img 20G
```

### 启动 guest OS
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
-drive if=none,format=qcow2,file=/home/jipeng/vms/ubuntu_desktop_20.04.6.img,id=disk0 \
-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=disk0,id=virtio-disk0,bootindex=1,write-cache=on \
-drive file=/home/jipeng/Downloads/iso/ubuntu-20.04.6-desktop-amd64.iso,file.locking=off,format=raw,if=none,id=drive-ide0-0-0,readonly=on \
-device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=2 \
-vnc 127.0.0.1:66 \
-monitor stdio
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
-vnc 0.0.0.0:1 \
-monitor stdio 
```

`-vnc`           指定 vnc 地址和端口，可使用 vnc viewer 连接，比如：192.168.74.83:5901
`-monitor stdio` 在启动 qemu 之后，进入交互式命令行，可执行 hmp 命令
  

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

# 配置网络
```bash
sudo brctl addbr br0
sudo brctl addif br0 eth0
sudo ifconfig eth0 0
sudo dhclient br0
sudo brctl show
sudo qemu-system-x86_64 -kernel linux/arch/x86/boot/bzImage \
       -append 'root=/dev/sda' -boot c -hda rootfs.img -k en-us \
       -net nic -net tap,ifname=tap0
```

# 使用 spice 实现宿主机与虚拟机共享剪贴板
1 配置 spice
```xml
virsh edit <虚拟机名称>

<devices>
  ...
  <graphics type='spice' autoport='yes' listen='0.0.0.0'>
    <listen type='address'/>
  </graphics>
  <channel type='spicevmc'>
    <target type='virtio' name='com.redhat.spice.0'/>
  </channel>
  ...
</devices>
```
`type='spice'`：指定使用 SPICE 协议。
`autoport='yes'`：自动分配 SPICE 端口。
`<channel>` 元素用于启用 SPICE VMC 通道，支持剪贴板共享等功能。

2 宿主机安装 spice 客户端
```bash
sudo apt-get update
sudo apt-get install virt-viewer
virt-viewer
```

3 虚拟机内安装 spice 工具
```bash
sudo apt-get install spice-vdagent
sudo systemctl enable spice-vdagent
sudo systemctl start spice-vdagent
```


[QEMU Guest Agent Protocol Reference](https://qemu.readthedocs.io/en/latest/interop/qemu-ga-ref.html)
