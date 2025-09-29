// 匹配守卫提供额外的条件
// 匹配守卫是个指定于 match 分支模式之后的额外的 if 条件，必须满足才能选择此分支。

fn fake_main1() {
    let num = Some(4);
    match num {
        Some(x) if x < 5 => println!("<5"),
        Some(x) => println!("x: {}", x),
        None => (),
    };
}

fn fake_main2() {
    let num = Some(4);
    let y = 10; // 位置1
    match num {
        Some(x) if x==y => println!("num == y"),  // 此处的 y 是位置 1 的 y
        Some(x) => println!("x: {}", x),
        None => (),
    }

    let x = 3;
    let y = false;
    match x {
        1|2|3 if y => println("1"),  // 相当于 (1|2|3) if y
        _ => println!("6"),
    }
}
