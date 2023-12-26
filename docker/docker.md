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
docker run -ti --privileged --network host --name ovt -v $PWD:$PWD -w $PWD debian12:x86_64 /bin/bash

# build systemd
git clone https://github.com/systemd/systemd
# ./configure --auto-features=disabled \
#             --default-library=static \
#             -D standalone-binaries=true \
#             -D static-libsystemd=true \
#             -D static-libudev=true \
#             -D link-udev-shared=false \
#             -D link-systemctl-shared=false \
#             -D link-networkd-shared=false \
#             -D link-timesyncd-shared=false \
#             -D link-boot-shared=false \
#             -D link-journalctl-shared=false \
#             -D link-portabled-shared=false \
#             -D prefer_static=true

./configure --auto-features=disabled \
            --default-library=static \
            -D static-libsystemd=true \
            -D static-libudev=true
make -j$(nproc)
make install

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
# docker build --network=host -t fedoar37:win64 -f fedoar37_win64.dockerfile .
# docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD fedoar37:win64 /bin/bash

# docker build --network=host -t debian10:win64 -f debian10_win64.dockerfile .
# docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian10:win64 /bin/bash

docker build --network=host -t debian12:win64 -f debian12_win64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian12:win64 /bin/bash


# 修改代码
git cherry-pick -x 410542d4a2d7c1d8136d3e49fc3ca29fbb76789a
git revert 0ec976f781fe1959303c5cd58ee85b98aefeb7c3

# 删除
qga/commands-win32.c
DEFINE_GUID(GUID_DEVINTERFACE_DISK,
        0x53f56307L, 0xb6bf, 0x11d0, 0x94, 0xf2,
        0x00, 0xa0, 0xc9, 0x1e, 0xfb, 0x8b);
DEFINE_GUID(GUID_DEVINTERFACE_STORAGEPORT,
        0x2accfe60L, 0xc130, 0x11d2, 0xb0, 0x82,
        0x00, 0xa0, 0xc9, 0x1e, 0xfb, 0x8b);


./configure  \
--with-vss-sdk="/home/jipeng/qemu-elf/" \
--cross-prefix=x86_64-w64-mingw32.static- \
--enable-guest-agent \
--disable-guest-agent-msi \
--enable-tools \
--disable-system \
--disable-werror

make -j$(nproc) qemu-ga qga/vss-win32/qga-vss.dll
```


# 进入容器，退出容器停止
docker attach {docker id}
# 进入容器，退出容器不停止
docker exec -it {docker id} bash
```
