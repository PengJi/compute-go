// 枚举

// 枚举类型的定义
// 1. 类似于 C 语言的方式
enum IpAddrKind {
    V4,
    V6,
}
struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

// 2. rust 提倡的方式
enum IpAddr2 {
    V4(String),  // 字符串
    V6(String),
}

// 3. 可以是不同的类型
enum IpAddr3 {
    V4(u8, u8, u8, u8),  // 元组
    V6(String),
}

// 4. 经典用法
enum Message {
    Quit,
    Move{x: i32, y: i32},  // 结构体
    Write(String),
    Change(i32, i32, i32),  // 元组
}
// 上面类似于
// struct QuitMessage;  // 类单元结构体
// struct MoveMessage {
//     x: i32,
//     y: i32,
// }
// struct WriteMessage(String)
// struct Change(i32, i32, i32)

// 5. 枚举类型的方式及 match
impl Message {
    fn prin(&self) {
        match *self {  // * 相当于解引用，match 相当于 switch
            Message::Quit => println!("Quit"),
            Message::Move{x, y} => println!("Change x = {}, y = {}", x, y),
            Message::Change(a, b, c) => println!("Change a = {}, b = {}, c = {}", a, b, c),
            _ => println!("Write")  // 默认值
            // Message::Write(&s) => println!("Write = {}", s)
        }
    }
}

fn main() {
    // C 语言方式
    let i1 = IpAddr {
        kind: IpAddrKind::v4,
        address: String::from("127.0.0.1"),
    }

    let i2 = IpAddr {
        kink: IpAddrKind::V6,
        address: String::from("2001:0db8:85a3:0000:0000:8a2e:0370:7334"),
    }

    // rust 方式
    let i1 = IpAddr2::V4(String::from("127.0.0.1");
    let i2 = IpAddr2::V6(String::from("2001:0db8:85a3:0000:0000:8a2e:0370:7334");

    let i1 = IpAddr3::V4(127, 0, 0, 1);  // 元组
    let i2 = IpAddr3::V6(String::from("2001:0db8:85a3:0000:0000:8a2e:0370:7334");

    let quit = Message::Quit;
    quit.prin();
    let mo = Message::Move{x: 10, y: 20};
    mo.prin();
    let wri = Message:Write(String::from("hello");
    wri.prin();
    let change = Message::Change(1, 2, 3);
    change.prin();
}
