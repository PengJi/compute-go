```bash
git clone git@github.com:spdk/spdk.git
cd spdk
git submodule update --init

# 下载依赖的包
./scripts/pkgdep.sh

# 配置并编译
./configure
make -j20

# 配置
sudo ./scripts/setup.sh

# 生成 nvme 盘的配置文件
sudo ./scripts/gen_nvme.sh --json-with-subsystems > ./build/examples/hello_bdev.json

cat ./build/examples/hello_bdev.json
{
"subsystems": [
{
"subsystem": "bdev",
"config": [
{
"method": "bdev_nvme_attach_controller",
"params": {
"trtype": "PCIe",
"name":"Nvme0",
"traddr":"0000:07:00.0"
}
}
]
}
]
}

sudo ./build/examples/hello_bdev --json ./build/examples/hello_bdev.json -b Nvme0

# 使用 vhost
sudo ./build/bin/vhost -c ./build/examples/hello_bdev.json
sudo ./scripts/spdkcli.py
sudo ./scripts/rpc.py bdev_malloc_create 64 512 -b malloc0
sudo ./scripts/spdkcli.py ls
```