使用 qemu 调试内核

# 编译 kernel
参考 [linux/kernel.md](linux/kernel.md)

# 制作根文件系统
参考 [linux/rootfs.md](linux/rootfs.md)

# 编译 qemu
参考 [qemu.md](qemu.md)

# 启动 qemu
```bash
cd linux-build
qemu-system-x86_64 \
-enable-kvm \
-cpu host \
-smp 1 \
-m 512M \
-kernel ./linux-4.19.297/arch/x86/boot/bzImage \
-drive file=rootfs.ext4,format=raw \
-append "root=/dev/sda rootfstype=ext4 console=tty1 console=ttyS0 nokaslr rw" \
-serial stdio \
-net nic \
-net user \
 -net nic -net tap,ifname=tap0 \
-s
```
`-s` 在1234端口接受GDB调试
`-S` 冻结CPU直到远程GDB输入相应命令

如果发现文件系统是只读的，可以在启动参数中添加`rw`选项

# 启动 GDB 调试
```bash
cd linux-build
gdb ./linux-4.19.297/vmlinux
(gdb) target remote localhost:1234
(gdb) b start_kernel #在入口函数 start_kernel 上打断点
(gdb) c
(gdb) layout src
```

# 其他
## 添加共享磁盘
在宿主机和qemu虚拟机之间共享文件
```bash
dd if=/dev/zero of=share.img bs=512 count=131072
mkfs.ext4 share.img
```
qemu 添加命令行，`-hdb share.img`
qemu 启动之后，在 VM 中挂载
```bash
mkdir share
mount /dev/sdb/ share
```
在主机上同样挂载文件，`sudo mount -t ext4 -o loop share.img ./share`

注意：如果 share 中的文件改变，则需要在 VM 或主机中重新 umount/mount。

[通过QEMU+GDB调试Linux内核](https://github.com/beacer/notes/blob/master/kernel/kernel-qemu-gdb.md)
