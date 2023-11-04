// 访问或者修改可变静态变量
// 静态变量和常量的区别：
// 1. 静态变量有一个固定的内存地址（使用这个值总会访问相同的地址），常量则允许在任何被用到的时候复制其数据。
// 2. 静态变量可以使可变的，尽管这可能是不安全的（用 unsafe 包含）

static HELLO_WORLD: &str = "hello, world";

static mut COUNTER: u32 = 0;  // 可变的静态变量
fn add_counter(inc: u32) {
    unsafe {
        COUNTER += inc;  // 不安全的代码
    }
}

fn main() {
    println!("{}", HELLO_WORLD);

    add_counter(3);
    add_counter(2);
    unsafe {
        println!("counter: {}", COUNTER);
    }
}
