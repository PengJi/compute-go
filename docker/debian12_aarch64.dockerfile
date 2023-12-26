FROM debian:bookworm-slim

USER root

RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list.d/debian.sources

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -yy apt-transport-https eatmydata

RUN dpkg --add-architecture arm64

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive eatmydata \
    apt install -y --no-install-recommends \
    crossbuild-essential-arm64 \
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
    gcc \
    python3-pip \
    gcc-aarch64-linux-gnu \
    binutils-aarch64-linux-gnu \
    linux-libc-dev:amd64 \
    libglib2.0-dev:arm64 \
    libpixman-1-dev:arm64 \
    libbz2-dev:arm64 \
    liblzo2-dev:arm64 \
    librdmacm-dev:arm64 \
    libsnappy-dev:arm64 \
    libxen-dev:arm64

RUN mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old && pip install Jinja2

WORKDIR /
