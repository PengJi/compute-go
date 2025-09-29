// 忽略模式中的值

fn foo(_: i32, y: i32) {
    println!("y = {}", y);
}

trait A {
    fn bar(x: i32, y: i32);
}

struct B {}

impl A for B {
    fn bar(_: i32, y: i32) {
        println!("y = {}", y);
    }
}

fn fake_main1() {
    foo(1, 2);
    let numbers = (1, 2, 3, 4);
    match numbers {
        (one, _, three, _) => {
            println!("one: {}, three: {}", one, three);
        },
    }
}

fn fake_main2() {
    // 如果变量没有用到，可以用下划线
    let _x = 5;
    let _y = 5;

    let s = Some(String::from("hello"));
    if let Some(_c) = s {  // 所有权发生转移，之后不能再使用 s
        println!("found a string");
    }
    // println!("s = {}", s);  //error

    let s = Some(String::from("hello"));
    if let Some(_) = s {  // 未发生所有权转移
        println!("found a string");
    }
    println!("s = {:?}", s);
}

fn fake_main2() {
    let numbers = (1, 2, 3);
    match numbers {
        (first, .., last) => {
            println!("first: {}, last: {}", first, last);
        }
    }

    // error
    // match numbers {
    //     (.., second, ..) => {
    //         println!("{}", second);
    //     }
    // }
}
