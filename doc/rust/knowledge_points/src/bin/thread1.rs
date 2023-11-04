// 线程

use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("num {} in spawn", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    // handle.join().unwrap();  // 等待线程执行完成才执行下面的代码

    for i in 1..5 {
        println!("num {} in main", i);
        thread::sleep(Duration::from_millis(1));
    }

    handle.join().unwrap();  // 等待线程执行完成程序才结束
}


// 1. 有两个并发概念内嵌于语言中：std::marker 中的 Sync 和 Send trait。
// 2. 通过 Send 允许在线程间转移所有权
//（1）Send 表明类型的所有权可以在线程间传递。几乎所有的 rust 类型都是 Send 的，但是例如 Rc<T> 是不能 Send 的。
//（2）任何完全由 Send 类型组成的类型也会自动被标记为 Send。
//struct A {
//	a
//	b
//	c
//}
//
// 3. Sync允许多线程访问
//（1）Sync 标记 trait 表明一个实现了 Sync 的类型可以安全的在多个线程中拥有其值的引用，
// 即对于任意类型 T，如果 &T（T 的引用）是 Send 的话 T 就是 Sync 的，
// 这意味着其引用就可以安全的发送到另一个线程。
//（2）智能指针 Rc<T> 也不是 Sync 的，出于其不是 Send 相同的原因。
// RefCell<T> 和 Cell<T> 系列类型不是 Sync 的。
// RefCell<T> 在运行时所进行的借用检查也不是线程安全的，Mutex<T> 是 Sync 的。
//
// 4. 手动实现 Send 和 Sync 是不安全的
// 通常并不需要手动实现 Send 和 Sync trait，因为由 Send 和 Sync 的类型组成的类型，
// 自动就是 Send 和 Sync 的。因为他们是标记 trait，甚至都不需要实现任何方法。
// 他们只是用来加强并发相关的不可变性的。
