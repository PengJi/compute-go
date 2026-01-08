# 使用 docker 部署 MySQL
```sh
# 初始化环境
docker pull mysql

# 创建 MySQL 数据目录
mkdir -p /home/jipeng/data/mysql

docker run -d \
--name some-mysql \
-v /home/jipeng/data/mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root \
mysql
```

```sh
# 使用（制作好的镜像，位于阿里云）
docker pull registry.cn-beijing.aliyuncs.com/mysql6/mysql:8.0.27-buster

# 创建 MySQL 数据目录
mkdir -p /home/jipeng/data/mysql

docker run -d \
--name some-mysql \
-v /home/jipeng/data/mysql:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root 
registry.cn-beijing.aliyuncs.com/mysql6/mysql:8.0.27-buster
```

## 部署MySQL8
```sh
# 拉取镜像
docker pull mysql:8.0

# 创建 MySQL 数据目录
mkdir -p /home/jipeng/data/mysql/data
mkdir -p /home/jipeng/data/mysql/conf
mkdir -p /home/jipeng/data/mysql/log

# 运行MySQL
docker run -d \
  --name mysql8 \
  --restart=always \
  --privileged=true \
  -p 3306:3306 \
  -v /home/jipeng/data/mysql/data:/var/lib/mysql \
  -v /home/jipeng/data/mysql/conf:/etc/mysql/conf.d \
  -v /home/jipeng/data/mysql/log:/var/log/mysql \
  -e MYSQL_ROOT_PASSWORD=root \
  -e TZ=Asia/Shanghai \
  -e MYSQL_ROOT_HOST='%' \
  mysql:8.0 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci
```

# 登录MySQL
```sh
# 在容器内登录MySQL
docker exec -it mysql8 bash
mysql -uroot -p

# 修改账号密码
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;

# 在本地登录MySQL
mysql -h 127.0.0.1 -P 3306 -u root -p
```

[docker mysql](https://hub.docker.com/_/mysql)  
