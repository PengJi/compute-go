# 安装 docker
## [在 ubuntu20.04 安装 docker]((https://docs.docker.com/engine/install/ubuntu/#install-from-a-package))
```bash
# 下载文件
wget \
https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/containerd.io_1.7.21-1_amd64.deb  \
https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/docker-ce_27.2.1-1~ubuntu.20.04~focal_amd64.deb \
https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/docker-ce-cli_27.2.1-1~ubuntu.20.04~focal_amd64.deb \
https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/docker-buildx-plugin_0.16.2-1~ubuntu.20.04~focal_amd64.deb \
https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/docker-compose-plugin_2.29.2-1~ubuntu.20.04~focal_amd64.deb
# 安装
sudo dpkg -i containerd.io_1.7.21-1_amd64.deb \
  docker-ce_27.2.1-1~ubuntu.20.04~focal_amd64.deb \
  docker-ce-cli_27.2.1-1~ubuntu.20.04~focal_amd64.deb \
  docker-buildx-plugin_0.16.2-1~ubuntu.20.04~focal_amd64.deb \
  docker-compose-plugin_2.29.2-1~ubuntu.20.04~focal_amd64.deb
# 不需要 sudo 运行 docker
# https://docs.docker.com/engine/install/linux-postinstall/
```

# 镜像代理加速
[DaoCloud/public-image-mirror](https://github.com/DaoCloud/public-image-mirror)

# 常用命令
```bash
# 构建镜像
docker build --network=host -t ovt:debian -f ovt-debian.dockerfile .

# 拉取镜像
docker pull registry.smtx.io/svt/svt:debian-svt-base

# 进入容器，退出容器停止
docker attach {docker id}

# 进入容器，退出容器不停止
docker exec -it {docker id} bash

# 打包镜像
docker save 0fdf2b4c26d3 > hangge_server.tar 
#或 
docker save -o images.tar postgres:9.6 mongo:3.4
docker load < hangge_server.tar
docker tag 3ab6782a4b2b svt:debian-svt-win64
```
