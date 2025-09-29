多线程 web server，优雅停机与清理
1. `cargo run`
2. 创建3个请求
```sh
for i in {1..3}
do
    curl http://127.0.0.1:7878/
done
```

执行结果类似如下：
请求端
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Rust</p>
  </body>
</html>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Rust</p>
  </body>
</html>
curl: (7) Failed to connect to 127.0.0.1 port 7878: Connection refused
```
服务端只可处理连个请求，第三个请求会被拒绝。

服务端
```
Worker 0 got a job; executing.
Shutting down.
Sending terminate message to all workers.
Shutting down all workers.
Shutting down worker 0
Worker 2 got a job; executing.
Worker 2 was told to terminate.
Worker 1 was told to terminate.
Worker 3 was told to terminate.
Worker 0 was told to terminate.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```
从上述信息可以看出，Worker 0 和 Worker 2 获取到请求并处理，处理完之后，ThreadPool 会停止并进入 Drop 的处理流程。
线程池通知所有线程终止，每个 worker 在接收到 Terminal 消息时，会打印一个信息，接着线程池调用 join 来终止每一个线程。
