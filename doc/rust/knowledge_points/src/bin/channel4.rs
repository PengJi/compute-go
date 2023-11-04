// 通道

// 多个生产者单个消费者

use std::thread;
use std::sync::mpsc;
use std::time::Duration;

fn main() {
    let (tx, rs) = mpsc::channel();
    let tx1 = mpsc::Sender::clone(&tx);
    let tx2 = mpsc::Sender::clone(&tx);

    thread::spawn(move || {
        let vals = vec![
            String::from("a");
            String::from("b");
            String::from("c");
            String::from("d");
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        let vals = vec![
            String::from("1");
            String::from("2");
            String::from("3");
            String::from("4");
        ];

        for val in vals {
            tx1.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    });

    thread::spawn(move || {
        let vals = vec![
            String::from("A");
            String::from("B");
            String::from("C");
            String::from("D");
        ];

        for val in vals {
            tx2.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    };)

    for rec in rx {
        println!("Got {}", rec);
    }
}
