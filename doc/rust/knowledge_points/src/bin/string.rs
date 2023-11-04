// 字符串

fn main {
    // 1. 创建一个空 String
    let mut s0 = String::new();
    s0.push_str("hello");
    println!("s0 = {}", s0);

    // 2. 通过字面值创建一个 String
    // 2.1 使用 String::from
    let s1 = String::from("some string");
    println!("{}", s1);
    // 2.2 使用 str 的方式
    let s1 = "some string".to_string();
    println!("{}", s1);

    // 3. 更新 String
    let mut s2 = String::from("hello");
    // 3.1 push_str
    s2.push_str(", world");
    let ss = " !".to_string();
    s2.push_str(&ss);
    println!("{}", s2);
    println!("ss = {}", ss);
    // 3.2 push
    let mut s2 = String::from("tea");
    s2.push('m');  // 只能添加单个字符，并且为单引号
    // s2.push('mx');  // error
    // s2.push("m");  // error
    println!("{}", s2);

    let s1 = "hello".to_string();
    let s2 = String::from(", world");
    let s2 = s1 + &s2;  // 注意：s2 为引用
    println!("s3 = {}", s3);
    // println!("s1 = {}", s1);  // error 所有权发生转移
    println!("s2 = {}", s2);

    // 3.4 使用宏 format!
    let s11 = String::from("11");
    let s22 = String::from("22");
    let s33 = String::from("33");
    let s44 = format!("{}-{}-{}", s11, s22, s33);  // 使用宏 format!，与 println! 类似
    println!("s44 = {}", s44);

    // 4. String 索引，使用字符
    // 5. str 索引，使用字节
    let s4= String::from("hello");
    // let s40 = s4[0];  // error
    println!("s4.len = {}", s4.len());
    
    let s4 = String:from("你好");  // 中文以 utf8 编码，一个中文占用 3 个字节
    println!("s4.len = {}", s4.len());
    println!("s4[0] = {}", &s4[0..3]);
    // println!("s4 = {}", &s4[0..2]);  // error，char 没有对齐

    // 6. 遍历
    // 6.1 chars
    for c in s4.chars() {
        println!("c = {}", c);
    }
    // 6.2 bytes
    for b in s4.bytes() {
        println!("b = {}", b);
    }
}
