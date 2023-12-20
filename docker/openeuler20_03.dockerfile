FROM openeuler/openeuler:20.03 AS python3-builder

USER root
RUN rm -f /etc/yum.repos.d/*
COPY openEuler.repo /etc/yum.repos.d/

RUN dnf clean all && dnf makecache && dnf update -y
RUN dnf install -y make autoconf bluez-libs-devel bzip2 bzip2-devel desktop-file-utils \
        expat-devel findutils gcc-c++ gcc gdbm-devel glibc-all-langpacks glibc-devel gmp-devel libappstream-glib libffi-devel \
        libnsl2-devel libtirpc-devel libGL-devel libuuid-devel libX11-devel ncurses-devel openssl-devel pkgconfig readline-devel\
        system-rpm-config tar tcl-devel tix-devel tk-devel xz-devel zlib-devel systemtap-sdt-devel net-tools sqlite-devel\
    && dnf clean all
RUN dnf update -y \
    && dnf install -y git rpmdevtools \
    && dnf clean all

WORKDIR /tmp/rpm