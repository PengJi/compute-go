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


# sed --in-place 's:-Dintrospection=disabled \\:-Dintrospection=disabled -Dfreetype=enabled -Dfontconfig=enabled \\:g' "src/pango.mk"
# rm src/cblas.mk src/lapack.mk src/armadillo.mk

# ENV TARGET x86-64

# # Add the foreign architecture we want and install dependencies
# # skip certificate verification(https://www.claudiokuenzler.com/blog/1088/how-to-solve-apt-error-server-certificate-verification-failed)
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C6BF758A33A3A276 && \
#     echo "deb https://pkg.mxe.cc/repos/apt stretch main" > /etc/apt/sources.list.d/mxeapt.list && \
#     echo 'Acquire::https::pkg.mxe.cc::Verify-Peer "false";' > /etc/apt/apt.conf.d/mxe-cert
# RUN apt-get update && \
#     DEBIAN_FRONTEND=noninteractive eatmydata \
#     apt-get install -y --no-install-recommends \
#         libpython2.7-stdlib \
#         msitools \
#         nsis \
#         $(apt-get -s install -y --no-install-recommends gw32.static-mingw-w64 | egrep "^Inst mxe-x86-64-unknown-" | cut -d\  -f2) \
#         mxe-$TARGET-w64-mingw32.static-bzip2 \
#         mxe-$TARGET-w64-mingw32.static-curl \
#         mxe-$TARGET-w64-mingw32.static-glib \
#         mxe-$TARGET-w64-mingw32.static-libgcrypt \
#         mxe-$TARGET-w64-mingw32.static-libssh2 \
#         mxe-$TARGET-w64-mingw32.static-libusb1 \
#         mxe-$TARGET-w64-mingw32.static-lzo \
#         mxe-$TARGET-w64-mingw32.static-nettle \
#         mxe-$TARGET-w64-mingw32.static-ncurses \
#         mxe-$TARGET-w64-mingw32.static-pixman \
#         mxe-$TARGET-w64-mingw32.static-pkgconf \
#         mxe-$TARGET-w64-mingw32.static-pthreads \
#         mxe-$TARGET-w64-mingw32.static-sdl2 \
#         mxe-$TARGET-w64-mingw32.static-sdl2-mixer \
#         mxe-$TARGET-w64-mingw32.static-sdl2-gfx \
#         mxe-$TARGET-w64-mingw32.static-zlib

# # Specify the cross prefix for this image (see tests/docker/common.rc)
# ENV PATH $PATH:/usr/lib/mxe/usr/bin/
# ENV QEMU_CONFIGURE_OPTS --cross-prefix=x86_64-w64-mingw32.static-

# RUN mkdir /tmp/qemu && \
#     mkdir /tmp/qemu/build

# WORKDIR /tmp/qemu

WORKDIR /
