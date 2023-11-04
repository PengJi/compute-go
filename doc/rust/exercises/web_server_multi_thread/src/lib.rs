use std::sync::mpsc;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

// 线程池（thread pool）是一组预先分配的等待或准备处理任务的线程。
// 当程序收到一个新任务，线程池中的一个线程会被分配任务，这个线程会离开并处理任务。
// 其余的线程则可用于处理在第一个线程处理任务的同时处理其他接收到的任务。
// 当第一个线程处理完任务时，它会返回空闲线程池中等待处理新任务。
// 线程池允许我们并发处理连接，增加 server 的吞吐量。
pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

trait FnBox {
    fn call_box(self: Box<Self>);
}

impl<F: FnOnce()> FnBox for F {
    fn call_box(self: Box<F>) {
        (*self)()
    }
}

// 类型别名
// job 用于存放通道中的代码（闭包）
type Job = Box<dyn FnBox + Send + 'static>;

impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// The size is the number of threads in the pool.
    ///
    /// # Panics
    ///
    /// The `new` function will panic if the size is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        // 创建通过，这里的通道相当于一个任务队列。
        // 通道的发送端是线程池的 execute，用于发送任务（闭包），接收端是 worker，用于从通道中获取任务并执行。
        let (sender, receiver) = mpsc::channel();

        // 由于多个线程需要从 receiver 获取代码，所以要保证线程安全。
        // 这里保证线程安全的方式为 Arc<Mutex<T>>。
        // Arc 使得多个接收端拥有 receiver。
        // Mutex 保证一次只有一个 worker 从接收端接收任务。
        let receiver = Arc::new(Mutex::new(receiver));

        // with_capacity 与 Vec::new() 作用类似，
        // 与 new() 的区别是为 vector 预分配空间，因此比 new() 更有效率。
        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            // 通过 Arc::clone 使得多个 worker 共享 receiver 的所有权。
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    // 闭包参数
    // 闭包作为参数可以有是三个不同的 trait：Fn、FnMut、FnOnce，因为处理请求的线程只会执行闭包一次，所以使用 FnOnce。
    // 这里的 FnOnce() 代表一个没有参数也没有返回值的闭包。
    // 使用 send 来将闭包从一个线程转移到另一个线程。
    // 使用 'static 是因为并不知道线程会执行多久。
    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        // 将要执行的代码发送到通道，之后 worker 会从通道接收任务
        self.sender.send(job).unwrap();
    }
}

// 标准库中的 spawn 在创建线程时，能够立即获取执行的代码（闭包）。
// 但若使用线程池的方式，是在创建线程后，之后才传入要执行的代码，我们需要实现这种方式。
// 具体实现方式是在 ThreadPool 和线程之间引入一个新的数据类型，即 Wroker。
// Wroker 负责在 ThreadPool 中将代码传递给线程
struct Worker {
    id: usize, // worker id，区别不同的 worker。
    // 在 spawn 中，spwn 返回的是 JoinHandle<T>，用于存放线程，这里由于传入的闭包不返回任何值，所以 T 为()。
    thread: thread::JoinHandle<()>,
}

impl Worker {
    // 所有的 worker 共享同一个 receiver，并且线程在修改 receiver 时需要是线程安全的。
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                // 从通道中获取需要执行的代码
                let job = receiver.lock().unwrap().recv().unwrap();

                println!("Worker {} got a job; executing.", id);

                job.call_box();
            }
        });

        Worker { id, thread }
    }
}
