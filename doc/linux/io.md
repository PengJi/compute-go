I/O执行模型(I/O Execution Model，简称IO Model, IO模型)：
1. blocking IO
2. nonblocking IO
3. IO multiplexing
4. signal driven IO
5. asynchronous IO

当一个用户进程发出一个 read I/O 系统调用时，主要经历两个阶段：
1. 等待数据准备好 (Waiting for the data to be ready)；
2. 把数据从内核拷贝到用户进程中(Copying the data from the kernel to the process)；

上述五种IO模型在这两个阶段有不同的处理方式。需要注意，阻塞与非阻塞关注的是进程的执行状态：
阻塞：进程执行系统调用后会被阻塞
非阻塞：进程执行系统调用后不会被阻塞

同步和异步关注的是消息通信机制：
同步：用户进程与操作系统（设备驱动）之间的操作是经过双方协调的，步调一致的
异步：用户进程与操作系统（设备驱动）之间并不需要协调，都可以随意进行各自的操作

总结一下阻塞IO、非阻塞IO、同步IO、异步IO的特点：
* 阻塞IO：在用户进程发出IO系统调用后，进程会等待该IO操作完成，而使得进程的其他操作无法执行。
* 非阻塞IO：在用户进程发出IO系统调用后，如果数据没准备好，该IO操作会立即返回，之后进程可以进行其他操作；如果数据准备好了，用户进程会通过系统调用完成数据拷贝并接着进行数据处理。
* 同步IO：导致请求进程阻塞/等待，直到I/O操作完成。
* 异步IO：不会导致请求进程阻塞。

阻塞和非阻塞的区别在于内核数据还没准备好时，用户进程是否会阻塞（第一阶段是否阻塞）；同步与异步的区别在于当数据从内核copy到用户空间时，用户进程是否会阻塞/参与（第二阶段是否阻塞）。

阻塞IO（blocking IO），非阻塞IO（non-blocking IO），多路复用IO（IO multiplexing），信号驱动IO都属于同步IO（synchronous IO）。这四种模型都有一个共同点：在第二阶段阻塞/参与，也就是在真正IO操作 read 的时候需要用户进程参与，因此以上四种模型均称为同步IO模型。
异步 IO 是当用户进程发起IO操作之后，就直接返回做其它事情去了，直到内核发送一个通知，告诉用户进程说IO完成。在这整个过程中，用户进程完全没有被阻塞。

io_uring 是由 Jens Axboe 提供的异步 I/O 接口，io_uring围绕高效进行设计，采用一对共享内存 ringbuffer 用于应用和内核间通信，避免内存拷贝和系统调用。io_uring 的实现于 2019 年 5 月合并到了 Linux kernel 5.1 中。

[I/O 设备](http://rcore-os.cn/rCore-Tutorial-Book-v3/chapter9/1io-interface.html)  
