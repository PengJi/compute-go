// 线程安全

use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    // 会出错，因为无法保证拥有 v 的所有权
    // let handle = thread::spawn(|| {
    //     println!("v: {:?}", v);
    // });
    //
    // 在执行上述代码后，在这里执行 drop，会丢弃 v, 则上述代码会出错，为了避免这种错误，必须转移所有权 
    // drop(v);

    // 必须使用 move，转移所有权
    let handle = thread::spawn(move || {
        println!("v: {:?}", v);
    });

    handle.join().unwrap();
}
