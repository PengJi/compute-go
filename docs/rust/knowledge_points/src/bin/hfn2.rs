// 返回闭包

// 下面的写法错误
// fn return_clo() -> Fn(i32)->i32 {
//     |x| x+1
// }

fn return_clo() -> Box<dyn Fn(i32)->i32> {
    Box::new(|x| x+1)
}

fn main() {
    let c = return_clo();
    println!("1 +1 = {}", c(1));
    // 或者
    println!("1 +1 = {}", (*c)(1));
}
