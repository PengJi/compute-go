安装
[Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

常用命令
```bash
# 构建镜像
docker build --network=host -t ovt:debian -f ovt-debian.dockerfile .

# 拉取镜像
docker pull registry.smtx.io/svt/svt:debian-svt-base
```

build for x86_64
```bash
docker build --network=host -t debian12:x86_64 -f debian12_x86_64.dockerfile .
docker run -ti --privileged --network host --name ovt -v $PWD:$PWD -w $PWD debian12:x86_64 /bin/bash

# build systemd
git clone https://github.com/systemd/systemd
# ./configure -Dstatic-libsystemd=true -Dstatic-libudev=true
./configure --auto-features=disabled \
            --default-library=static \
            -D standalone-binaries=true \
            -D static-libsystemd=true \
            -D static-libudev=true \
            -D link-udev-shared=false \
            -D link-systemctl-shared=false \
            -D link-networkd-shared=false \
            -D link-timesyncd-shared=false \
            -D link-boot-shared=false \
            -D link-journalctl-shared=false \
            -D link-portabled-shared=false \
            -D prefer_static=true

./configure --auto-features=disabled \
            --default-library=static \
            -D static-libsystemd=true \
            -D static-libudev=true \
            -D prefer_static=true
make -j$(nproc)
make install

# build qemu-ga
./configure --static --target-list=x86_64-softmmu \
--enable-guest-agent \
--disable-docs \
--disable-debug-info \
--enable-cap-ng
make qemu-ga -j$(nproc)
```

build for aarch64
```bash
# aarch64
./configure --static --disable-docs --enable-guest-agent --target-list=aarch64-softmmu --cross-prefix=aarch64-linux-gnu-
make qemu-ga -j$(nproc)
```

build for win64
```bash
docker build --network=host -t fedoar37:win64 -f fedoar37_win64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD fedoar37:win64 /bin/bash

docker build --network=host -t debian10:win64 -f debian10_win64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian10:win64 /bin/bash

docker build --network=host -t debian12:win64 -f debian12_win64.dockerfile .
docker run -ti --privileged --network host -v $PWD:$PWD -w $PWD debian12:win64 /bin/bash

vsssdk='vsssdk_7.2.exe'
# curl -O http://192.168.67.2/distros/isostore/SVT/windows_install/${vsssdk}
wget https://download.microsoft.com/download/9/4/c/94c588cf-8176-4bdb-9d55-2597c76043c6/setup.exe -O ${vsssdk}
scripts/extract-vsssdk-headers ${vsssdk}

./configure  \
--with-vss-sdk \
--enable-guest-agent \
--disable-docs \
--cross-prefix=x86_64-w64-mingw32.static- \
--prefix="C:\\Program Files\\svt"

./configure  \
--with-vss-sdk \
--enable-guest-agent \
--disable-docs \
--host=x86_64-w64-mingw32.static \
"--prefix=C:\\Program Files\\svt"

make -j$(nproc) qemu-ga.exe qga/vss-win32/qga-vss.dll
```


# 进入容器，退出容器停止
docker attach {docker id}
# 进入容器，退出容器不停止
docker exec -it {docker id} bash
```
