使用 docker 部署 mysql
```bash
# 初始化环境
docker pull mysql
mkdir /home/jipeng/data/mysql
docker run --name some-mysql -v /home/jipeng/data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d mysql

# 使用（制作好的镜像，位于阿里云）
docker pull registry.cn-beijing.aliyuncs.com/mysql6/mysql:8.0.27-buster
mkdir  /home/jipeng/data/mysql
docker run --name some-mysql -v /home/jipeng/data/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d registry.cn-beijing.aliyuncs.com/mysql6/mysql:8.0.27-buster
docker exec -it some-mysql bash

# 远程连接 MySQL
docker run -it --rm mysql mysql -h172.17.0.2 -uroot -p
root
# 其他：docker run -it --network host --rm mysql mysql -hsome-mysql -uroot -p
```
