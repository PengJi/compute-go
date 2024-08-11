创建镜像
```sh
cd goweb/docker
docker build -f goweb.dockerfile -t registry.cn-beijing.aliyuncs.com/pengji/dev:goweb-v1 .
```

运行容器
```sh
docker run -d -p 8081:8080 registry.cn-beijing.aliyuncs.com/pengji/dev:goweb-v1
# 访问
http://127.0.0.1:8081/
# 测试数据库连接
http://127.0.0.1:8081/search/xiaoming
# 测试 ollama 连接
http://127.0.0.1:8081/v3/ollama/
```

配置文件
```sh
config/config.yaml
```

运行
```sh
go run main.go
```