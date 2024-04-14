安装
```bash
sudo apt purge bpfcc-tools libbpfcc python3-bpfcc
# ubuntu
sudo apt install -y zip bison build-essential cmake flex git libedit-dev \
  libllvm14 llvm-14-dev libclang-14-dev python3 zlib1g-dev libelf-dev libfl-dev python3-setuptools \
  liblzma-dev libdebuginfod-dev arping netperf iperf
wget https://github.com/iovisor/bcc/releases/download/v0.30.0/bcc-src-with-submodule.tar.gz
cd bcc-src-with-submodule
mkdir build
cd build
cmake ..
make
sudo make install
cmake -DCMAKE_INSTALL_PREFIX=/usr -DPYTHON_CMD=python3 ..  # build python3 binding
pushd src/python/
make
sudo make install
popd
export PYTHONPATH=$(dirname `find /usr/lib -name bcc`):$PYTHONPATH
```

[Ubuntu - Source](https://github.com/iovisor/bcc/blob/master/INSTALL.md#ubuntu---source)