// 默认泛型类型参数和运算符重载
//（1）使用泛型类型参数时，可以为泛型指定一个默认的具体类型。
//（2）运算符重载是指在特定情况下自定义运算符行为的操作。
// rust 并不允许创建自定义运算符或者重载运算符，
// 不过对于 std::ops 中列出的运算符和相应的 trait，我们可以实现运算符相关 trait 来重载。

use std::ops::Add;

// Add trait 定义如下
//trait Add<RHS=Self> { //尖括号里面为默认类型参数，RHS是一个泛型类型参数（right hand side）
//    type Output;
//    fn add(self, rhs: RHS) -> Self::Output;  // rhs 默认为 Self，这里通过 RHS=Self 显示指定为 Self，也可以指定为其他类型
//}

#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

// 泛型类型参数为 Self（默认值）
impl Add for Point {
    type Output = Point;
    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

#[derive(Debug)]
struct Millimeters(u32);
struct Meters(u32);
// 泛型类型参数为 Meters
impl Add<Meters> for Millimeters {
    type Output = Millimeters;
    fn add(self, other: Meters) -> Millimeters {
        Millimeters(self.0 + other.0 * 1000)
    }
}

fn main() {
    assert_eq!(Point{x: 1, y: 1} + Point{x: 2, y: 2}, Point{x: 3, y: 3});
    let mi = Millimeters(1);
    let m = Meters(1);
    let r = mi + m;
    println!("r = {:?}", r);
}
