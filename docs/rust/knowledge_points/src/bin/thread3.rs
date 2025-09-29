// 通道类似于但所有权的方式，值传递到通道后，发送者就无法再使用这个值；
// 共享内存类似于多所有权，即多个线程可以同时访问相同的内存位置。
//
// 互斥器：Mutex<T>
// 1. 任意时刻，只允许一个线程来访问某些数据；
// 2. 互斥器使用时，需要先获取到锁，使用后需要释放锁。

use std::sync::Mutex;

fn main() {
    // Mutex<T> 是一个只能指针，lock 调用返回一个 MutexGuard 的智能指针
    // 内部提供了 drop 方法，当 MutexGuard 离开作用域时自动释放锁
    let m = Mutex::new(0);
    {
        let mut num = m.lock().unwrap();
        *num = 6;
    }  // 离开作用于，自动释放锁

    println!("m = {}", m);
}
