# 基础概念
## socket
可以理解为主板上的一个插座, 用来连接物理 CPU 芯片到主板上, 简单讲, 有多少个 socket 就有多少个物理 CPU。在家用电脑上，主板上一般只有一个 socket，但是服务器上可能有多个 socket，比如 2 个，4 个，8 个，甚至更多。

## core
core 是将多个一样的 CPU 放置于一个封装内(或直接将两个 CPU 做成一个芯片), 每个这样的 CPU 叫做一个 core, 每个 core 是一个的独立的执行单元。
这里涉及了[多核技术](https://zh.wikipedia.org/wiki/%E5%A4%9A%E6%A0%B8%E5%BF%83%E8%99%95%E7%90%86%E5%99%A8)

## thread
thread 涉及到[超线程技术](https://zh.wikipedia.org/wiki/%E8%B6%85%E5%9F%B7%E8%A1%8C%E7%B7%92) ，简单的讲，就是把两个逻辑内核模拟成两个物理芯片, 让单个处理器都能使用线程级并行计算。

## 逻辑 CPU 数量
CPU 的数量不能简单的通过物理 CPU 的数量(或者 socket 的数量) 来判断, 如果用了多核技术, 则需要计算全部 core 的数量, 如果用了超线程, 则需要加上 所有 CPU 线程. 所以每一个 CPU(包括 core 或者 thread) 都叫一个逻辑 CPU.

## 一些查看方法
### 查看物理 cpu 数
`cat /proc/cpuinfo| grep "physical id"| sort| uniq| wc -l`

### 查看每个物理 cpu 中 核心数(core 数)
`cat /proc/cpuinfo | grep "cpu cores" | uniq`

### 查看总的逻辑 cpu 数（processor 数）
`cat /proc/cpuinfo| grep "processor"| wc -l`

### 查看 cpu 型号
`cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c`


## 举例
以一颗 intel 13700k CPU 为例。
```bash
cat /proc/cpuinfo
processor       : 0
physical id     : 0
siblings        : 24
core id         : 0
cpu cores       : 16

processor       : 1
physical id     : 0
siblings        : 24
core id         : 0
cpu cores       : 16
```
`processor`
表示逻辑 CPU 的 ID

`physical id`
物理 CPU(socket) 的 ID, 具有相同 physical id 的逻辑 CPU 在同一个 CPU 封装内

`siblings`
同一个 CPU 封装(socket)里的逻辑 CPU 数量, 这个数字表示在该物理 CPU 里面有多少个逻辑 CPU

`core id`
核心 ID, 具有相同 core id 的逻辑 CPU 在同一个 core 里, 即是使用了超线程的逻辑 CPU

`cpu cores`
CPU 核心数, 在该物理 CPU 内封装的 core 数目。

```bash
# 查看 socket，结果表明只有一个物理 CPU
cat /proc/cpuinfo | grep "physical id"
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0
physical id	: 0

# 结果表明使用了超线程技术，有些 CPU core （core id 相同）内可以有两个逻辑 CPU
cat /proc/cpuinfo | grep "core id"                    
core id		: 0
core id		: 0
core id		: 4
core id		: 4
core id		: 8
core id		: 8
core id		: 12
core id		: 12
core id		: 16
core id		: 16
core id		: 20
core id		: 20
core id		: 24
core id		: 24
core id		: 28
core id		: 28
core id		: 32
core id		: 33
core id		: 34
core id		: 35
core id		: 36
core id		: 37
core id		: 38
core id		: 39
```

# 通过 qemu 模拟多核 CPU
（1）模拟一个具有 1 个物理 CPU, 两个逻辑 CPU 的系统
```bash
qemu -enable-kvm -m 1024 ArchLinux.img -smp 2,sockets=1
```
guest 查看
```bash
$ cat /proc/cpuinfo
processor   : 0 physical id : 0 siblings    : 2 core id : 0 cpu cores   : 2  
processor   : 1 physical id : 0 siblings    : 2 core id : 1 cpu cores   : 2
```
可以看到两个逻辑 CPU 是双核的, 没有使用超线程技术。


（2）模拟一个具有 1 个物理 CPU(双核), 四个逻辑 CPU 的系统. 此时为了满足双核 四线程的概念, 得启用超线程技术
```bash
qemu -enable-kvm -m 1024 ArchLinux.img -smp 4,sockets=1,cores=2
```
guest 查看
```bash
$ cat /proc/cpuinfo
processor   : 0 physical id : 0 siblings    : 4 core id : 0 cpu cores   : 2  
processor   : 1 physical id : 0 siblings    : 4 core id : 0 cpu cores   : 2  
processor   : 2 physical id : 0 siblings    : 4 core id : 1 cpu cores   : 2  
processor   : 3 physical id : 0 siblings    : 4 core id : 1 cpu cores   : 2
```

（3）模拟一个具有 2 个物理 CPU, 四个逻辑 CPU 的系统, 启用超线程技术, 每个核心两个 线程. 不难算出, 此时每个 CPU 都是单核的(4 = 2*2*1)
```bash
qemu -enable-kvm -m 1024 ArchLinux.img -smp 4,sockets=2,threads=2
```
guest 查看
```bash
$ cat /proc/cpuinfo
processor   : 0 physical id : 0 siblings    : 2 core id : 0 cpu cores   : 1  
processor   : 1 physical id : 0 siblings    : 2 core id : 0 cpu cores   : 1  
processor   : 2 physical id : 1 siblings    : 2 core id : 0 cpu cores   : 1  
processor   : 3 physical id : 1 siblings    : 2 core id : 0 cpu cores   : 1
```

