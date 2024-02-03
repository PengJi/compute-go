
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

[kvm 虚拟机qcow2磁盘格式扩容](https://cpp.la/514.html)