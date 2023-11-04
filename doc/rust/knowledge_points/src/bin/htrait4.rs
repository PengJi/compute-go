// 父 trait 用于在另一个 trait 中使用某 trait 的功能。
// 有时我们可能需要再某个 trait 中使用另一个 trait 的功能，
// 在这种情况下，需要实现依赖相关的 trait。
// 这个所需的 trait 是我们实现的 trait 的父（超）trait（supertrait）。

use std::fmt;
trait OutPrint: fmt::Display {  // 要求实现 Display trait
    fn out_print(&self) {
        let output = self.to_string();
        println!("output: {}", output);
    }
}

struct Point {
    x: i32,
    y: i32,
}

impl OutPrint for Point {}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

fn main() {
    let p = Point{x: 1, y: 2};
    p.out_print();
}
