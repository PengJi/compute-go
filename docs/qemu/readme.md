使用 qemu + libvirt 创建虚拟机
1. 创建磁盘
```bash
qemu-img create -f qcow2 windows11-dev.qcow2 100G
```

2. 编写 xml
修改磁盘
修改iso

3. 启动虚拟机
启动虚拟机
```sh
sudo virsh define openeuler-20_03.xml
sudo virsh start openeuler-20_03
```

4. 通过 VNC 连接虚拟机
```sh
192.168.124.25:5900
```
