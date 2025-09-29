// 模式是 rust 中特殊的语法，模式用来匹配值的结构。 
// 模式由如下内容组成：
//（1）字面值
//（2）解构的数组、枚举、结构体或元组
//（3）变量
//（4）通配符
//（5）占位符

// match
// match VALUE {
//     PATTERN => EXPRESSION,
//     PATTERN => EXPRESSION,
// }
fn fake_main() {
    let a = 1;
    match a {  // 必须匹配完所有情况，即数据类型内的所有数
        0 => println!("zero"),
        1 => println!("one"),
        _ => println!("other"),
    };
}

// if let
fn main1() {
    let color: Option<&str> = None,
    let is_ok = true;
    let age: Result<u8, _> = "33".parse();

    if let Some(c) = color {
        println!("color: {}", c);
    } else if is_ok {
        println!("is ok");
    } else if let Ok(a) = age {
        if a > 30 {
            println!("greater than 30");
        } else {
            println!("less than 30");
        }
    } else {
        println!("else");
    }
}

// while let
// 只要模式匹配就一直执行 while 循环
fn fake_main2() {
    let mut stack = Vec::new();
    stack.push(1);
    stack.push(2);
    stack.push(3);

    // 只要匹配 Some(value) 就会一直循环
    while let Some(top) = stack.pop() {
        println!("top = {}", top);
    }
}

// for
// 在for循环中，模式是直接跟随for关键字的值，例如 for x in y，x就是对应的模式
fn fake_main3() {
    let v = vec!['a', 'b', 'c'];
    
    // 模式为 (index, value)
    for (index, value) in v.iter().enumerate() {
        println!("index = {}, value = {}", index, value);
    }
}
 
// let
// let PATTERN = EXPRESSION
fn fake_main4() {
    let (x, y, z) = (1, 2, 3); // (1, ,2, 3) 会匹配（x, y, z），将 1 绑定到 x，依次类推
    println!("x = {}, y = {}, z = {}", x, y, z);
}

// 函数
// 函数的参数也是模式
fn print_point(&(x, y): &(i32, i32)) {
    println!("x = {}, y = {}", x, y);
}
fn fake_main5() {
    let p = (3, 5);
    print_point(&p);  // &(3, 5) 匹配模式 &(x, y)  
}

//模式在使用它的地方并不都是相同的，模式存在不可反驳的和可反驳的
