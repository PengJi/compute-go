// 对象：数据和操作数据的过程
// 结构体、枚举类型与 impl 块，实现对象

use getaver;

fn main() {
    let mut a = getaver::AverCollect::new();
    a.add(1);
    println!("averget = {}", a.average());

    a.add(2);
    println!("average = {}", a.average());

    a.add(3);
    println!("average = {}", a.average());

    a.remove();
    println!("average = {}", a.average());
}
