// 控制流

fn main() {
    // if - else if - else
    let n = 2;
    if n == 1 {
        println!("n == 1");
    } else if n == 2 {
        println!("n == 2");
    } else {
        println!("other");
    }

    // 在 let 中使用 if
    let condition = true;
    let x = if condition {
        5 
    } else {
        6
        // "six" // error
    }

    // for
    let arr:[u32; 5] = [1, 2, 3, 4, 5];
    for n in arr.iter() {
        println!("element = {}", n);
    }

    // while
    let mut i = 10;
    while i != 10 {
        i += 1;
    }
    println!("i == {}", i);

    // loop
    let mut cnt = 0;
    loop {
        println!("in loop");
        if cnt == 10 {
            break;
        }

        cnt += 1;
    }
    println!("res = {}", res);

    let res = loop {
        cnt += 1;
        if cnt == 20 {
            break cnt * 2;
        }
    }
    println!("res = {}", res);
}
