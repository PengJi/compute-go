// Option

// 1. Option 是标准库定义的一个枚举，形式：
// enum Option<T> {
//     Some(T),
//     None,
// }
// T 是一个泛型

// 2. 使用方式
fn main() {
    let some_number = Some(5);
    let some_string = Some(String::from("a string"));
    let absent_number: Option<i32> = None;

    let x: i32 = 5;
    let y: Option<i32> = Some(5);
    let mut temp = 0;
    match y {  // match 匹配值，一定要匹配完所有元素
        Some(i) => {temp = i; }
        None => {println!("do something");}
    }

    let sum = x + temp;  // 必须经过 match 才能相加
    println!("sum = {}", sum);

    // let result = plus_one(y);
    // match result {
    //     Some(i) => println!("result = {}", i),
    //     None => println!("nothing"),
    // };
    
    // 只配置一个元素
    if let Some(value) = plus_one(y) {
        println!("value = {}", value);
    }

    // 替代 match
    if let Some(value) = plus_one(y) {
        println!("value = {}", value);
    } else {
        println!("do nothing");
    }
}

// option 函数
fn plus_one(x: Option<i32) -> Option<i32> {
    match x {
        Some(x) => Some(x+1),  
        None => None,     
    }
}
