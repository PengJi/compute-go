创建镜像
```sh
cd goweb/docker
docker build -f goweb.dockerfile -t registry.cn-beijing.aliyuncs.com/pengji/dev:goweb-v1 .
```

配置文件
```sh
config/config.yaml
```

运行
```sh
go run main.go
```