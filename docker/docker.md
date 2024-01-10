安装
[Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

常用命令
```bash
# 构建镜像
docker build --network=host -t ovt:debian -f ovt-debian.dockerfile .

# 拉取镜像
docker pull registry.smtx.io/svt/svt:debian-svt-base
```

# build for x86_64
```bash
docker build --network=host -t debian12:x86_64 -f debian12_x86_64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian12:x86_64 /bin/bash

# build qemu-ga
./configure --static \
--target-list=x86_64-softmmu \
--enable-guest-agent \
--disable-docs \
--disable-debug-info \
--disable-gnutls
make qemu-ga -j$(nproc)
```

# build for aarch64
```bash
docker build --network=host -t debian12:aarch64 -f debian12_aarch64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian12:aarch64 /bin/bash

# aarch64
./configure --static --target-list=aarch64-softmmu \
--enable-guest-agent \
--disable-docs \
--disable-gnutls \
--cross-prefix=aarch64-linux-gnu-
make qemu-ga -j$(nproc)
```

# build for win64
```bash
docker build --network=host -t debian12:win64 -f debian12_win64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian12:win64 /bin/bash

./configure  \
--with-vss-sdk="/home/jipeng/qemu-elf/" \
--cross-prefix=x86_64-w64-mingw32.static- \
--enable-guest-agent \
--disable-guest-agent-msi \
--enable-tools \
--disable-system \
--disable-werror

make -j$(nproc) qemu-ga qga/vss-win32/qga-vss.dll

scp -T build/qga/qemu-ga.exe smtxauto@192.168.31.37:'"C:\program files\svt\qemu-ga.exe"'

```


# 进入容器，退出容器停止
docker attach {docker id}
# 进入容器，退出容器不停止
docker exec -it {docker id} bash
```
