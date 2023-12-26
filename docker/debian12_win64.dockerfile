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
    cd /opt/mxe && \
    wget -P /opt/mxe/pkg ... && \
    make cc MXE_TARGETS='x86_64-w64-mingw32.static' --jobs=8 JOBS=8 && \
    make glib MXE_TARGETS='x86_64-w64-mingw32.static' --jobs=8 JOBS=8

ENV PATH=$PATH:/opt/mxe/usr/bin/

# build vsssdk
ENV VSSSDK='vsssdk_7.2.exe'
RUN wget -O ${VSSSDK} https://download.microsoft.com/download/9/4/c/94c588cf-8176-4bdb-9d55-2597c76043c6/setup.exe
RUN scripts/extract-vsssdk-headers ${VSSSDK}

WORKDIR /
