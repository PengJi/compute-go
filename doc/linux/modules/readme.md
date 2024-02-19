编译 kvm
```bash
cp /boot/config-4.19.90-2307.3.0.oe1.smartx.33.x86_64 ./.config
make olddefconfig
make -j$(nproc) -> compile.log
make modules SUBDIRS=arch/x86/kvm

# 卸载旧版本 kvm
modprobe -r kvm_intel && modprobe -r kvm

# 安装新版本 kvm
modprobe irqbypass && insmod kvm.ko && insmod kvm-intel.ko
```

