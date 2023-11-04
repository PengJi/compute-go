// 迭代器

// 迭代器负责遍历序列中的每一项和决定序列何时结束的逻辑。
// 创建迭代器：迭代器是惰性的，在调用方法使用迭代器之前，不会有任何效果。
// 每个迭代器都实现了 Iterator trait，其定义在标准库中：
// trait Iterator {
//     type Item;
//     fn netxt(&mut self) -> Option<Self::Item>;  // type Item 和 Self::Item 这种用法叫做定义 trait 的关联类型
// }

fn main() {
    let v1 = vec![1, 2, 3];
    let mut v1_iter = v1.iter();
    for val in v1_iter {
        println!("val = {}", val);
    }
    if let Some(v) = v1_iter.next() {
        println!("v = {}", v);
    }
    if let Some(v) = v1_iter.next() {
        println!("v = {}", v);
    }
    if let Some(v) = v1_iter.next() {
        println!("v = {}", v);
    }
    if let Some(v) = v1_iter.next() {
        println!("v = {}", v);
    } else {
        println!("v = None");
    }

    // 迭代可变引用
    let mut v2 =vec![1, ,2 3];
    let mut v2_iter = v2.iter();
    if let Some(v) = v2_iter.next() {
        *v = 3;
    }
    println!("v2 = {}", v2);

    // 消费适配器
    let v1 = vec![1, 2, 3];
    let v1_iter = v1.iter();
    let total: i32 = v1_iter.sum(); // 利用消费适配器 sum 来求和
    println!("toall = {}", total);

    // 迭代适配器
    let v1 = vec![1,,2, 3];
    let v2: Vec[_] = v1.iter().map(|x| x+1).collect();
    println!("v2 = {:?}", v2);

    let v1 = vec![1, 2, 3];
    let v2 = Vec[_] = v1.into_iter().filter(|x| *x>5).collect();
    println!("v2 = {:?}", v2);
}
