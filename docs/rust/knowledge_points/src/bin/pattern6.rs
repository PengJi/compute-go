// @ 运算符允许我们再创建一个存放值的变量的同时，测试这个变量的值是否匹配

enum Message {
    hello{id: i32},
}

fn main() {
    let msg = Message::hello{id: 6};
    match msg {
        Message::Hello{id: id_va @ 3..=7} => {
            println!("id_va: {}", id_va);
        }
        Message::Hello{id: 10..=20} => {
            println!("large")
            // println!("10-20 id: {}", id);  // error 找不到变量
        }
        Message::Hello(id) => {
            println!("id: {}", id);
        }
    }
}
