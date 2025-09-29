# 编译安装 qemu、
编译安装
```bash
cd qemu-7.0.0
./configure \
--prefix=/usr \
--target-list=riscv64-softmmu,riscv64-linux-user,x86_64-softmmu,x86_64-linux-user \
--enable-sdl && \
make -j && \
sudo make install
```

验证
```bash
qemu-system-x86_64 --version
```

# 编译安装 libvirt
编译安装
```bash
cd libvirt
git checkout v8.0.0

meson build \
--prefix=/usr \
--buildtype=debug \
--debug && \
ninja -C build && \
sudo ninja -C build install
```

启动服务
```bash
sudo systemctl start libvirtd
```

# 安装 vmtools
```bash
sudo apt install qemu-guest-agent
```

# 获取 IP 地址
```bash
sudo virsh qemu-agent-command ubuntu-20_04 --pretty '{"execute": "guest-network-get-interfaces"}'
```

# 使用 vnc
```bash
# 获取 vnc 地址
echo $(hostname -I | awk '{print $1}'):5900
```
