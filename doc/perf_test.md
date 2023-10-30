
# 存储性能
```bash
# 持续 30s
fio -name=testio -filename=/data/fiotest -bs=256k -direct=1 -iodepth=128 -rw=randrw -ioengine=libaio -size=10G -threads=3 -time_based -runtime=30 -output=/data/log
```

# 网络性能
## 开启服务端
```bash
iperf -s
```
## 客户端测试
```bash
iperf -c {server ip} -f m -i 1 -t 30
```
参数：
-s,--server：iperf 服务器模式，默认启动的监听端口为5201，eg：iperf -s
-c,--client host：iperf客户端模式，host是server端地址，eg：iperf -c 222.35.11.23
-i，--interval：指定每次报告之间的时间间隔，单位为秒，eg：iperf3 -c 192.168.12.168 -i 2
-p，--port：指定服务器端监听的端口或客户端所连接的端口，默认是5001端口。
-u，--udp：表示采用UDP协议发送报文，不带该参数表示采用TCP协议。
-l，--len：设置读写缓冲区的长度，单位为 Byte。TCP方式默认为8KB，UDP方式默认为1470字节。通常测试 PPS 的时候该值为16，测试BPS时该值为1400。
-b，--bandwidth [K|M|G]：指定UDP模式使用的带宽，单位bits/sec，默认值是1 Mbit/sec。
-t，--time：指定数据传输的总时间，即在指定的时间内，重复发送指定长度的数据包。默认10秒。
-A：CPU亲和性，可以将具体的iperf3进程绑定对应编号的逻辑CPU，避免iperf进程在不同的CPU间调度。
