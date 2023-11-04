// 解引用

// 需要实现 Deref trait。
// let a: A = A::new();
// let b = &b;
// let c = *b;  // 解引用

// 实现Deref trait允许我们重载解引用运算符。
//let a: A = A::new();//前提：A类型必须实现Deref trait
//let b = &a;
//let c = *b;//解引用

fn main() {
    let x = 5;
    let y = &x;
    assert_eq!(5, x);
    assert_eq!(5, *y);  // 解引用

    let z = Box::new(x); // 使用 Box，new 的时候发生了 copy，将数据放在堆上
    assert_eq!(5, *z);

    let m = Box::new(String::from("rust"));
    hello(&m);  // 将 MyBox 变为 &String，再将 String 的解引用，变为字符串 slice。
}

fn hello(name: &str) {
    println!("hello {}", name);
}

// 解引用多态与可变性交互：
//（1）当 T：Deref<Target=U> 时，从 &T 到 &U
//（2）当 T：DerefMut<Target=U> 时，从 &mut T 到 &mut U
//（3）当 T：Deref<Target=U> 时，从 &mut T 到 &U
