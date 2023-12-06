安装
[Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

常用命令
```bash
# 构建镜像
docker build --network=host -t ovt:test -f ovt.dockerfile .


# 拉取镜像
docker pull registry.smtx.io/svt/svt:debian-svt-base

# 运行容器
docker run --rm -ti --privileged --network host --name ovt -v $PWD:$PWD -w $PWD ovt:test /bin/bash


# 进入容器，退出容器停止
docker attach {docker id}
# 进入容器，退出容器不停止
docker exec -it {docker id} bash
```
