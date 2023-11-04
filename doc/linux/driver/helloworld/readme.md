1. 编写 heloworld 驱动代码；
helloworld_dev.c

2. 编写 Makefile；
执行 `make`

3. 编译和安装 hellwrold 驱动；
a. 编译驱动 `make`
编译之后会生成 `helloworld_dev.ko` 文件

b. 安装驱动 `insmode helloworld_dev.ko`
查看内核信息
```
Message from syslogd@jp-dev at Nov 19 16:26:55 ...
kernel:register_chrdev_region ok

Message from syslogd@jp-dev at Nov 19 16:26:55 ...
kernel: hello driver init
```
上述信息表明驱动注册与初始化成功。

c. 查看驱动
执行 `lsmod`
```
Module                  Size  Used by
helloworld_dev         16384  0
```
驱动已经安装。目前该驱动还没有被使用。

d. 卸载驱动
执行 `rmmod helloworld_dev.ko`

3. 生成驱动文件
执行 `mknod /dev/helloworld c 232 0`
`/dev/helloworld` 设备名称
`c`               设备类型为字符设备
`232`             主设备号
`0`               从设备号

4. 应用程序使用 helloworld 驱动；
a. 编译应用程序 `gcc -o test test_helloworld.c`
b. 执行应用程序 `./test`
输出
```
3
open successe
0 0
```

查看内核输出 `dmesg`
```
[4474848.489791] hello_open
[4474848.491373] hello_write
[4474848.491977] hello_read
```
上述说明调用了驱动的函数 `hello_open`、`hello_write`、`hello_read`。
