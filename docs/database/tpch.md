使用 tpc-h 测试 mysql
# 下载 TPC-H
[https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp)

# 构建测试数据
```bash
# 解压 tpch
$ unzip TPC-H-Tool.zip
$ cd TPC-H_V3.0.1


#修改 Makefile 文件中的 CC、DATABASE、MACHINE 和 WORKLOAD 等参数定义。
$ cp makefile.suite Makefile
$ vim Makefile
CC      = gcc  # 修改
Current values for DATABASE are: INFORMIX, DB2, TDAT (Teradata)
                                 SQLSERVER, SYBASE, ORACLE, VECTORWISE
Current values for MACHINE are:  ATT, DOS, HP, IBM, ICL, MVS,
                                 SGI, SUN, U2200, VMS, LINUX, WIN32
Current values for WORKLOAD are:  TPCH
DATABASE= MYSQL  # 修改
MACHINE = LINUX  # 修改
WORKLOAD = TPCH  # 修改


# 修改 tpcd.h 文件，并添加新的宏定义。
$ vim tpcd.h
#ifdef MYSQL
#define GEN_QUERY_PLAN ""
#define START_TRAN "START TRANSACTION"
#define END_TRAN "COMMIT"
#define SET_OUTPUT ""
#define SET_ROWCOUNT "limit %d;\n"
#define SET_DBASE "use %s;\n"
#endif


# 编译生成 dbgen
$ make
```

编译完成后该目录下会生成以下两个可执行文件：
* dbgen：数据生成工具。
* qgen：SQL 生成工具。生成初始化测试查询，由于不同的 seed 生成的查询不同，为了结果的可重复性，请使用附件提供的 22 个查询。

dbgen 命令可以生成指定大小的数据，生成环境测试建议不少于 1000G 。以 10G 为例。
```bash
$ ./dbgen -s 10
TPC-H Population Generator (Version 3.0.0)
Copyright Transaction Processing Performance Council 1994 - 2010
```

# 导入数据
```bash
mysql -uroot --local-infile

# 创建数据库
create database TPCD;
use TPCD;

# 创建表
\. /home/jipeng/TPC-H_V3.0.1/dbgen/dss.ddl

# 创建索引、外键等
vim dss.ri
-- CONNECT TO TPCD;  # 修改
# 运行
\. /home/jipeng/TPC-H_V3.0.1/dbgen/dss.ri

# 将表名改为小写
rename table CUSTOMER to customer;
rename table LINEITEM to lineitem;
rename table NATION to nation;
rename table ORDERS to orders;
rename table PART to part;
rename table PARTSUPP to partsupp;
rename table REGION to region;
rename table SUPPLIER to supplier;

# 导入数据
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/part.tbl' into table part fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/region.tbl' into table region fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/nation.tbl' into table nation fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/customer.tbl' into table customer fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/supplier.tbl' into table supplier fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/orders.tbl' into table orders fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/partsupp.tbl' into table partsupp fields terminated by '|';
load data local infile '/home/jipeng/TPC-H_V3.0.1/dbgen/lineitem.tbl' into table lineitem fields terminated by '|';
```

# 执行测试
```bash
vim tpch-benchmark-olap.sh
#!/bin/bash
exec 3>&1 4>&2 1>> tpch-benchmark-olap-`date +'%Y%m%d%H%M%S'`.log 2>&1
I=1
II=3
while [ $I -le $II ]
do
N=1
T=23
while [ $N -lt $T ]
do
  if [ $N -lt 10 ] ; then
    NN='0'$N
  else
    NN=$N
  fi
  echo "query $NN starting"
  time mysql -uroot -DTPCD < ./queries/${NN}.sql
  echo "query $NN ended!"
  N=`expr $N + 1`
  echo -e
  echo -e
done
 I=`expr $I + 1`
done
```

# 其他
### 问题1
导入数据时报错：
```bash
mysql> load data local infile '/tmp/part.tbl' into table part fields terminated by '|';
ERROR 3948 (42000): Loading local data is disabled; this must be enabled on both the client and server sides
```
解决：
要解决 `ERROR 3948 (42000): Loading local data is disabled` 错误，并启用 `LOAD DATA LOCAL INFILE` 功能，你需要在客户端和服务器两端都启用该功能。以下是详细步骤：

#### 在服务器端启用 `LOCAL INFILE`

1. **编辑 MySQL 配置文件**

   编辑 MySQL 配置文件（例如 `my.cnf` 或 `my.ini`），添加或修改以下内容：

   ```ini
   [mysqld]
   local_infile=1
   ```

2. **重启 MySQL 服务器**

   重启 MySQL 服务器以应用配置更改。

   ```sh
   # For systemd-based systems:
   sudo systemctl restart mysql

   # For init.d-based systems:
   sudo service mysql restart
   ```

#### 在客户端启用 `LOCAL INFILE`

客户端也需要启用 `LOCAL INFILE`。有几种不同的方法可以在客户端启用它。

1. 使用命令行参数

在使用 `mysql` 客户端时，添加 `--local-infile` 参数：

```sh
mysql --local-infile -u username -p
```

1. 在 MySQL 客户端会话中启用

在登录到 MySQL 之后，可以使用以下命令启用 `LOCAL INFILE`：

```sql
SET GLOBAL local_infile = 1;
```
