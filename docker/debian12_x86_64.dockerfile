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
    meson \
    gperf \
    python3-pip \
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

RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old && pip install Jinja2

# build systemd for static library of libudev
RUN git clone https://github.com/systemd/systemd /opt/systemd && \
    ./configure \
    --auto-features=disabled \
    --default-library=static \
    -D static-libsystemd=true \
    -D static-libudev=true && \
    make -j$(nproc) && \
    make install

WORKDIR /
