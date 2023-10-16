在 ubuntu 编译内核
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
cd linux-4.19
# make mrproper会删除配置的.config以及其他备份
sudo make mrproper
# make clean会删除编译过程中生成的中间文件和内核镜像文件
sudo make clean
```

4. 配置内核
```bash
cd linux-4.19
# 使用图像化配置模块，当前目录下生成一个 .config 文件
sudo make menuconfig
# 使用默认配置，当前目录下生成一个 .config 文件
# make defconfig
# 检查配置的依赖关系是否正确
# make oldconfig
```

修改 .config
```bash
修改为
CONFIG_SYSTEM_TRUSTED_KEYS=""
```

5. 编译
```bash
# 编译内核镜像及其他所有模块
sudo make -j$(nproc)

# 单独编译
# 编译内核镜像
sudo make bzImage -j$(nproc)
# 编译其他所有模块
sudo make modules -j$(nproc)
```

注意：ubuntu 20.04 默认安装的是 gcc-9，编译内核时会报错，需要安装 gcc-8
```bash
sudo apt install gcc-8 g++-8
# 设置为默认编译器
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 800 --slave /usr/bin/g++ g++ /usr/bin/g++-8
``` 
参考：[How To Install gcc-8 Only on Ubuntu 18.04](https://devicetests.com/install-gcc-8-ubuntu-18-04)

6. 生成内核镜像
在 `arch/x86/boot` 会生成 bzImage 文件，这是一个压缩的内核镜像。

