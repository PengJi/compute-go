FROM debian:bookworm-slim

USER root

RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list.d/debian.sources
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -yy apt-transport-https eatmydata

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    eatmydata apt-get dist-upgrade -y && \
    eatmydata apt-get install --no-install-recommends -y \
    gnupg \
    dirmngr \
    software-properties-common \
    msitools \
    autoconf \
    autopoint \
    automake \
    libtool \
    meson \
    bison \
    flex \
    bzip2 \
    zip \
    git \
    wget \
    gperf \
    curl \
    vim \
    nsis \
    python3 \
    python3-distutils \
    python3-pkg-resources \
    python-is-python3 \
    pkg-config \
    ninja-build \
    build-essential \
    cmake \
    ca-certificates \
    openssl \
    ruby \
    libtool-bin \
    lzip \
    p7zip-full \
    libgdk-pixbuf2.0-dev \
    libssl-dev \
    intltool \
    python3-mako \
    bash \
    g++ \
    g++-multilib \
    gettext \
    libc6-dev-i386 \
    libgdk-pixbuf2.0-dev \
    libltdl-dev \
    libgl-dev \
    libpcre3-dev \
    libssl-dev \
    libtool-bin \
    libxml-parser-perl \
    patch \
    perl \
    unzip \
    xz-utils \
    wixl

# build mxe, tutorial: https://mxe.cc/#tutorial
RUN git clone https://github.com/mxe/mxe.git /opt/mxe && \
    cd /opt/mxe && mkdir pkg && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/binutils-2.38.tar.bz2 && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/ccache-3.6.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/gcc-11.4.0.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/gmp-6.2.1.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/isl-0.16.1.tar.bz2 && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/libtool-2.4.6.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/mingw-w64-v11.0.1.tar.bz2 && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/mpc-1.2.1.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/mpfr-4.1.0.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/pkgconf-da179fd.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/ninja-v1.11.1.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/cmake-3.28.1.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/meson-1.2.1.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/dbus-1.15.6.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/expat-2.5.0.tar.bz2 && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/gettext-0.21.1.tar.lz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/libiconv-1.17.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/libffi-3.3.tar.gz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/pcre-8.45.tar.bz2 && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/zlib-v1.3.tar.xz && \
    # wget -P /opt/mxe/pkg http://192.168.17.20/repo/pub/smartxos/iso/vmtools/windows_build/glib-2.70.2.tar.xz && \
    make cc MXE_TARGETS='x86_64-w64-mingw32.static' --jobs=10 JOBS=10 && \
    make glib MXE_TARGETS='x86_64-w64-mingw32.static' --jobs=10 JOBS=10

ENV PATH=$PATH:/opt/mxe/usr/bin/

ENV VSSSDK='vsssdk_7.2.exe'
RUN wget -O ${VSSSDK} https://download.microsoft.com/download/9/4/c/94c588cf-8176-4bdb-9d55-2597c76043c6/setup.exe && \
    scripts/extract-vsssdk-headers ${VSSSDK}

RUN mkdir /tmp/qemu && \
    mkdir /tmp/qemu/build

WORKDIR /tmp/qemu
