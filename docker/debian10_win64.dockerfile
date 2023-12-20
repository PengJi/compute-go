FROM debian:buster-slim

USER root

RUN cat /etc/apt/sources.list | sed "s/^deb\ /deb-src /" >> /etc/apt/sources.list
RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list
RUN sed -i '/security.debian.org/d' /etc/apt/sources.list

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -yy apt-transport-https eatmydata && \
    eatmydata apt install -y \
    autoconf \
    automake \
    libtool \
    pkg-config \
    ninja-build \
    build-essential \
    ca-certificates \
    bison \
    flex \
    git \
    software-properties-common \
    lsb-release \
    msitools \
    libglib2.0-dev

# Install MXE from the binary distribution
# ref: https://mxe.cc/#tutorial
RUN apt-key adv \
    --keyserver hkp://keyserver.ubuntu.com:80 \
    --recv-keys 86B72ED9 && \
    add-apt-repository \
    "deb [arch=amd64] https://pkg.mxe.cc/repos/apt `lsb_release -sc` main" && \
    apt-get update && \
    apt install -y \
    mxe-x86-64-w64-mingw32.static-cc

ENV PATH=/usr/lib/mxe/usr/bin:$PATH

WORKDIR /
