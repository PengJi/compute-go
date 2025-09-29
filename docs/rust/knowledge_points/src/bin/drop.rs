// Drop trait 类似于其他语言中的析构函数，当值离开作用域的时候执行此函数的代码。

struct Dog {
    name: String,
    // count:: i32,
}

impl Drop for Dog {
    fn drop(&mut self) {
        println!("Dropping Dog: {}", self.name);
        // self.count -= 1;
    }
}

//rust提供了std::mem::drop()
fn main() {
    let a = Dog{name: String::from("dog1")};
    {
        let b = Dog{name: String::from("dog2")};
        println!("0000000000000000000");
    }

    // drop(a);  // 手动释放对象

    println!("11111111111111111111111");
}
