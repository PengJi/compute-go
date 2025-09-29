// 通道

// 发送者的 send 方法返回的是一个 Result<T, E>。
// 如果接收端被丢弃了，将没有发送目标，此时会返回发送错误。
// 接收者的 recv 返回值也是一个 Result<T, E>。
// 当发送端关闭时，返回错误。
// 接收端使用 recv，消息到来前会一直阻塞。可以使用 try_recv()，不会阻塞，立即返回。
//
// rust 中实现消息传递并发的主要工具是通道，通道由两部分组成，分别是发送端和接收端。
// 发送端和接收端任一被丢弃时，都认为通道被关闭了。
//
// 通过 mpsc::channel 创建通道，多个生成者，单个消费者；
// 通过 spmc::channel 创建通道，单个生产者，多个消费者；
// 示例：
// let (tx, rx) = mpsc::channel();
// let (tx, rx) = spmc::channel();

use std::thread;
use std::sync::mpsc;

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let val = String::from("hi");
        tx.send(val).unwrap();
    }

    let received = rx.recv().unwrap();  // 接收到消息之前，会阻塞到这里
    println!("Got {}", received);   
}
