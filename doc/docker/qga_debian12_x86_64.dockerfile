FROM debian:bookworm-slim

USER root

RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list.d/debian.sources

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -yy apt-transport-https eatmydata

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    eatmydata apt-get dist-upgrade -y && \
    eatmydata apt-get install --no-install-recommends -y \
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
    curl \
    wget \
    meson \
    gperf \
    gettext-base \
    psmisc \
    texinfo \
    makeself \
    genisoimage \
    xorriso \
    python3-jinja2 \
    # selinux-policy-dev \
    libglib2.0-dev \
    libmspack-dev \
    libpam0g-dev \
    libssl-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libx11-dev \
    libxext-dev \
    libxinerama-dev \
    libxi-dev \
    libxrender-dev \
    libxrandr-dev \
    libxtst-dev \
    libgtk-3-dev \
    libgtkmm-3.0-dev \
    libudev-dev \
    libunistring-dev \
    libcap-dev \
    libcap-ng-dev

# build systemd for static library of libudev
RUN wget -P /opt/ http://192.168.17.20/repo/pub/smartxos/iso/vmtools/build_assets/systemd-255.tar.gz &&\
    tar -xf /opt/systemd-255.tar.gz -C /opt/ &&\
    cd /opt/systemd-255 &&\
    ./configure \
    --buildtype=release \
    --auto-features=disabled \
    --default-library=static \
    -D static-libsystemd=true \
    -D static-libudev=true \
    -D mode=release && \
    make -j$(nproc) && \
    make install

RUN mkdir /tmp/qemu

WORKDIR /tmp/qemu
