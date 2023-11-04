// 模式有两种：refutable（可反驳的）和 irrefutable（不可反驳的）。能
// 匹配任何传递的可能值的模式被称为是不可反驳的。
// 只能接受不可反驳模式的有：函数、let语句、for循环。原因：因为通过不匹配的值程序无法进行有意义的工作。
// 对值进行匹配可能会失败的模式被称为可反驳的。
// if let 和 while let 表达式被限制为只能接受可反驳的模式，因为它们的定义就是为了处理有可能失败的条件。

// 匹配字面值
fn fake_main1() {
    let x = 1;
    match x {
        1 => println!("one"),
        2 => println!("two"),
        - => println!("-"),
    };
}

// 匹配命名变量
fn fake_main2() {
    let x = Some(5);  // 位置2
    let y = 10;  // 位置1
    match x {
        Some(50) => println!("50"),
        Some(y) => println!("value = {}", y),  // 此处的 y 不是位置1 的 y
        _ => println!("other"),
    }

    println!("x = {}, y = {}", x, y);  // 此处的 y 是位置 1 的 y
}

// 多个模式
fn fake_main3() {
    let x = 1;
    match x {
        1|2 = > println!("1 or 2"),  // 或，匹配 1 或者 2
        3 => println!("3"),
        - => println!("x"),
    }
}

// 通过 .. 匹配
fn fake_main4() {
    let x = 5;
    match x {
        1..=5 => println!("1 to 5"),  // 1|2|3|4|5 => println!("1 to 5"),
        _ => println!("x"),
    }
    
    let x = 'c';
    match x {
        'a'..='j' => println!("1"),
        'k'..='z' => println!("2"),
        _ => println!("other"),
    }
}
