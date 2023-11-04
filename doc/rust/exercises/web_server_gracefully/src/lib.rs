use std::sync::mpsc;
use std::sync::Arc;
use std::sync::Mutex;
use std::thread;

trait FnBox {
    fn call_box(self: Box<Self>);
}

impl<F: FnOnce()> FnBox for F {
    fn call_box(self: Box<F>) {
        (*self)()
    }
}

type Job = Box<dyn FnBox + Send + 'static>;

// Message 要么是存放了线程需要运行的 Job 的 NewJob 成员，要么是使线程退出循环并终止的 Terminate
enum Message {
    NewJob(Job),
    Terminate,
}

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Message>,
}

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

        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));
        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.send(Message::NewJob(job)).unwrap();
    }
}

// 为 threadpool 实现 Drop，当线程池被关闭时，应该 join 所有线程以确保它们完成操作
impl Drop for ThreadPool {
    fn drop(&mut self) {
        println!("Sending terminate message to all workers.");

        // 向每个 worker 发送 Terminate 消息
        for _ in &mut self.workers {
            self.sender.send(Message::Terminate).unwrap();
        }

        println!("Shutting down all workers.");

        // 遍历线程池中的所有 worker
        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            // 使用 let 解构 Some，如果存在 thread 则取出，如果为 None，则不做操作
            // 调用 take 将 thread 移动出 worker
            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }

        // 上述遍历了两次 workers，如果放在一个循环中，将会有如下问题：
        // 在一个单独的循环中遍历每个 worker，在第一次迭代中向信道发送 Terminate 并对第一个 worker 调用 join，
        // 如果此时第一个 worker 正在处理请求，则第二个 worker 将会收到 Terminate 并停止，
        // 这样我们会一直等待第一个 worker 结束，但由于第二个 worker 接收了 Terminate 所以它并不会收到信号，
        // 从而不会停止。
        // 
        // 为了避免上述情况，首先在一个循环中向信道发出所有 Terminate 消息，接着在另一个循环中 join 所有线程，
        // 每个 worker 一旦收到 Terminate 消息则停止从信息接收消息，这里 Terminate 消息数同 worker 数目相同，
        // 可确保每个 worker 都会收到一个终止消息。
    }
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Message>>>) -> Worker {
        let thread = thread::spawn(move || loop {
            // 从信道中接收 Message，根据不同的 Message 做不同的处理
            let message = receiver.lock().unwrap().recv().unwrap();

            match message {
                Message::NewJob(job) => {  // 执行任务
                    println!("Worker {} got a job; executing.", id);
                    job.call_box();
                }
                Message::Terminate => {  // 终止
                    println!("Worker {} was told to terminate.", id);
                    break;
                }
            }
        });

        Worker {
            id,
            thread: Some(thread),
        }
    }
}
