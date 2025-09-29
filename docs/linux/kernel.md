编译 linux kernel
操作系统 ubuntu 22.04，`Linux dev 5.15.0-87-generic #97-Ubuntu SMP Mon Oct 2 21:09:21 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux`  
编译器 `gcc (Ubuntu 8.4.0-3ubuntu2) 8.4.0`
kernel 版本 `https://mirrors.tuna.tsinghua.edu.cn/kernel/`

1. 安装依赖
```bash
sudo apt install gcc-8 g++ libncurses5-dev build-essential \
kernel-package libssl-dev libc6-dev bin86 flex bison qttools5-dev \
libelf-dev zstd
```

2. 下载内核源码
```bash
wget https://mirrors.tuna.tsinghua.edu.cn/kernel/v4.x/linux-4.19.tar.gz
tar -xvf linux-4.19.tar.gz
```

3. 编译前清理
```bash
cd inux-4.19
make clean
```

其他 make 选项
```bash
#  删除所有生成的文件、配置 .config 和各种各样备份的文件
make mrproper
# make clea n会删除编译过程中生成的中间文件和内核镜像文件，但保留配置文件和足够的构建外部模块的构建支持
make clean
# 相当于执行一次 make mrproper，然后再删除编辑器备份和补丁文件
make distclean

# make distclean > make mrproper > make clean

# 使用已有的 .config，但会询问新增的配置项
# 它会在现有的内核配置文件基础上建立一个新的配置文件，只会向用户提供有关新内核特性的问题。在新内核升级的过程中，它会非常有用，
# 用户将现有的配置文件 .config 复制到新内核的源码中，执行 make oldconfig，此时，用户只需要回答新增特性的问题即可。
make oldconfig

# 与 make oldconfig 一样，只是额外悄悄地更新选项的依赖关系。
make silentoldconfig

# 与 make silentoldconfig 一样，但不需要手动交互，而是对新选项以其默认值进行配置。
make olddefconfig

# 基于 X Window 的一种配置方式，提供了漂亮的配置窗口，不过只能在 X Server 上运行 X 桌面应用程序时使用，它依赖于 QT。
make xconfig

# 使用默认配置，当前目录下生成一个 .config 文件
# 按照内核中提供的默认配置文件对内核进行配置，在 intel x86——64 平台上，默认配置文件为 arch/x86/configs/x86_64_defconfig，
# 生成的 .config 文件可以用作初始化配置，然后使用 make menuconfig 或 make xconfig 进行配置。
make defconfig
```

4. 配置内核
为了确保生成的 .config 文件生成的内核是实际可以工作的（直接 make defconfig 生成的 .config 文件编译出来的内核常常不能工作），
最佳实践是以当前使用的 config (位于目录 /boot，比如 /boot/config-5.15.0-87-generic）为基础，将它复制到 linux 目录下，
重命名为 .config，然后通过 make olddefconfig 来更新 .config 文件，这样可以确保生成的 .config 文件是可用的。
```bash
cd linux-4.19
# 根据现有的配置文件生成新的配置文件
cp /boot/config-5.15.0-87-generic /home/jipeng/linux/.config
make olddefconfig
# 或者使用图像化配置模块，当前目录下生成一个 .config 文件
make menuconfig
```

或者修改 .config 配置文件，开启 virtio 相关的模块。
```bash
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

CONFIG_SYSTEM_TRUSTED_KEYS=""
CONFIG_SYSTEM_REVOCATION_KEYS=""

# 需默认开启的模块
# https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/about/
```

5. 编译
```bash
# 编译内核镜像及其他所有模块
make -j$(nproc) -> compile.log
```
有时候编译完成之后，并不会生成 `vmlinux` 文件，这里将编译过程中的正常日志保存到 `compile.log` 文件，错误信息会直接打印出来，可以根据错误信息进行排查。


单独编译
```bash
# 编译内核镜像
sudo make bzImage -j$(nproc)
# 编译其他所有模块
sudo make modules -j$(nproc)
```

编译内核完成之后在 `/arch/x86/boot/` 目录下生成 `bzImage` 文件。


# 问题
注意：ubuntu 20.04 默认安装的是 gcc-9，编译内核时会报错，需要安装 gcc-8
```bash
sudo apt install gcc-8 g++-8
# 设置为默认编译器
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8
``` 
参考：[How To Install gcc-8 Only on Ubuntu 18.04](https://devicetests.com/install-gcc-8-ubuntu-18-04)