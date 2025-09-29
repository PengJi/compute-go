// 解构并分解值
// 解构元组、结构体、枚举、引用

// 解构结构体
struct Point {
    x: i32,
    y: i32,
}

fn fake_main1() {
    let p = Point { x: 1, y: 2 };
    let Point{x: a, y: b} = p;  //变量 a 和变量 b 匹配 x 和 y
    assert_eq!(1, a);
    assert_eq!(2, b);

    let Point{x, y} = p;
    assert_eq!(1, x);
    assert_eq!(2, y);

    let p = Point { x: 1, y: 0 }
    match p {
        Point{x, y:0} => println!("x axis"),
        Point{x:0, y} => println!("y axis"),
        Point{x, y} => println!("other"),
    };
}

// 解构枚举
enum Message {
    Quit,
    Move{x: i32, y: i32},
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn fake_main2() {
    let msg = Message::ChangeColor(0, 1, 2);
    match msg {
        Message::Quit => {
            println!("quit");
        }
        Message::Move(x, y) => {
            println!("move, x: {}, y: {}", x, y);            
        }
        Message::Write(text) => println!("write msg: {}", text),
        Message::ChangeColor(r, g, b) => {
            println!("color, r:{}, g:{}, b:{}", r, g, b);
        }
    }    
}

enum Color {
    Rgb(i32, i32, i32),
    Hsv(i32, i32, i32),
}

enum Message {
    Quit,
    Move{x: i32, y: i32},
    Write(String),
    ChangeColor(Color),
}

fn fake_main3() {
    let msg = Message::ChangeColor(Color::Hsv(0, 1, 2));
    match msg {
        Message::ChangeColor(Color::Rgb(r, g, b)) => {
            println!("rgb color, r: {}, g: {}, b: {}", r, g, b);
        }
        Message::ChangeColor(Color::Hsv(h, s, v)) => {
            println!("hsv color, h: {}, s: {}, v: {}", h, s, v);
        }
        _ => ()
    }
}

// 解构元组
struct Point {
    x: i32,
    y: i32,
}

fn fake_main4() {
    let ((a, b), Point{x, y}) = ((1, 2), Point(x: 3, y: 4));
    println!("a: {}, b: {}, x: {}, y: {}", a, b, x, y);
}
