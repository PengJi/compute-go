Rust 异步

async/.await 为 Rust 内置编写异步的工具。  
async 将一个代码块转化为实现了 future 特征的状态机。  
转化为 future 后，当在同步方法中调用阻塞函数（async函数），会阻塞整个线程，但是阻塞的 future 会让出线程控制权，允许其他 future 运行。  

[Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/01_getting_started/01_chapter.html)
