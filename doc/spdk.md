```bash
git clone git@github.com:spdk/spdk.git
cd spdk
git submodule update --init

# Prerequisites
./scripts/pkgdep.sh

./configure
make
```

```bash
sudo ./scripts/setup.sh

sudo ./scripts/gen_nvme.sh --json-with-subsystems > ./build/examples/hello_bdev.json
```