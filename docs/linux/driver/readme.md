驱动编写

# 配置驱动开发环境(centos8)
```bash
# 安装内核开发
sudo yum install -y kernel-devel-$(uname -r) kernel-headers-$(uname -r)
sudo yum install elfutils-libelf-devel

ln -s /usr/src/kernels/$(uname -r)/ /lib/modules/$(uname -r)/build
ll /lib/modules/$(uname -r)/build
```
