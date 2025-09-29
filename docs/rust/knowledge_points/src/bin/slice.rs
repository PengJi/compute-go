// 切片

// 1、字符串 slice 是 String 中一部分值的引用，所以要使用 &
// 2、字面值就是 slice
// 3、其它类型 slice

fn main() {
    // 字符串 slice
    let s= String::from("hello world");

    let h = &s[0..5];
    let h = &s[0..=4];
    let h = &s[..=4];
    let h = &s[..5];
    println!("h = {}", h);  // hello

    let w = &s[6..11];
    let w = &s[6..=10];
    let w = &s[6..];
    let w = &s[..];
    println!("w = {}", w);  // world

    // 字面值 slice
    // let ss = String::from("你好");
    // let w1 = &ss[0..1];  // error, 字节必须是对齐的，中为一个字符占用4个字节，所以应该为 0..5

    // 其他类型的 slice
    let arr = [1, 2, 3, 4, 5];
    let ss = &a[1..3];
    println!("ss = {}", ss[0]);
    println!("ss = {}", ss[1]);
    println!("len= {}", ss.len());  // 2
}
