
```bash
sudo rmmod kvm_amd kvm
sudo insmod ./arch/x86/kvm/kvm.ko
sudo insmod ./arch/x86/kvm/kvm-intel.ko
sudo insmod ./arch/x86/kvm/kvm-amd.ko

make M=./arch/x86/kvm/ modules -j$(nproc)

make -j$(nproc) -C `pwd` M=`pwd`/arch/x86/kvm modules

kernel_version=linux-4.19.90-2204.4.0.0146.oe1.x86_64
cd /usr/src/${kernel_version}/arch/x86/kvm
KDIR="/lib/modules/$(uname -r)/build"
make -j$(nproc) -C ${KDIR} M=$(pwd) modules


#######################
obj-m := gpt-dump.o
PWD := $(shell pwd)
KDIR := /lib/modules/$(shell uname -r)/build

all:
	make -C $(KDIR) M=$(PWD) modules
clean:
	make -C $(KDIR) M=$(PWD) clean

#######################
# 进入 KVM 代码目录
cd /root/kernel-src/kvm-2.6.32/arch/x86/kvm

# 开始编译 
make -C /lib/modules/`uname -r`/build M=`pwd` clean
make -C /lib/modules/`uname -r`/build M=`pwd` modules

# 拷贝编译结果出来，并使用
cp *.ko /root/kvm/tools/modules/
cd /root/kvm/tools/modules/

# 卸载旧版本模块
modprobe -r kvm_intel
modprobe -r kvm

# 安装新版本模块
modprobe irqbypass
insmod kvm.ko
insmod kvm-intel.ko


```
