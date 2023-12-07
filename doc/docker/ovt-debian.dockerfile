FROM debian:bookworm-slim

USER root

RUN sed -i 's\http://deb.debian.org/\http://mirrors.tuna.tsinghua.edu.cn/\' /etc/apt/sources.list.d/debian.sources
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -yy apt-transport-https eatmydata
RUN DEBIAN_FRONTEND=noninteractive eatmydata \
    apt install -y autoconf automake libtool pkg-config \
    build-essential \
    ca-certificates \
    bison \
    flex \
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
    libgtkmm-3.0-dev

WORKDIR /
