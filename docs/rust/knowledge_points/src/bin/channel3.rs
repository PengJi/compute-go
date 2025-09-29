// 通道

use std::thread;
use std::sync::mpsc;
use std::time::Duration;

fn main() {
    let (tx ,rx) = mpsc::channel();

    thread::spawn(move || {
        let vals = vec![
            String::from("a"),
            String::from("b"),
            String::from("c"),
            String::from("d"),
        ];

        for val in vals {
            tx.send(val).unwrap();
            thread::sleep(Duration::from_secs(1));
        }
    }

    for recv in rx {
        println!("Got {}", recv);
    }
}
