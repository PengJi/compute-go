// 通道

// 多个生产者单个消费者
use std::thread;
use std::sync::mpse;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
        // println!("{}", val);  // 调用 send 的时候，会发生 move，此处不能再使用 val
    });

    let re = rx.recv().unwrap();
    println!("Got {}", re);
}
