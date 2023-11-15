// 结构体中的生命周期
// 在某些情况下没有生命周期注解也能够编译。
/// 
// 符合以下三条规则（适用于函数及方法）则可省略生命周期注解：
// （1）每个引用的参数都有它自己的生命周期参数，例如：
// 一个引用参数的函数，有一个生命周期：fn foo<'a>(x: &'a i32))
// 两个引用参数的函数，有两个生命周期：fn foo<'a, 'b>(x: &'a i32, y: &'b i32)
// 以此类推
// （2）如果只有一个输入生命周期参数，那么它被赋予所有输出生命周期参数：
// fn foo(x: &i32) -> &i32 等价于 fn foo<'a>(x: &'a i32) -> &'a i32
// （3） 如果方法有多个输入生命周期参数，不过其中之一因为方法的缘故为 &self 或者 &mut self，
// 那么 self 的生命周期被赋予所有输出生命周期参数，例如：
// fn foo(&self, x: &str, y: &str, ....) -> &str
// 
// 如果不符合上述三条规则，并且没有指定生命周期注解，则编译器会停止并生成错误。

#[derive(Debug)]
struct A<'a> {
    name: &'a str,
}

// 生命周期省略
fn get_a_str(name: &str) -> &str {
    s
}

fn main() {
    let n = String::from("hello");
    let a = A {name: &n};
    println!("a = {:#?}", a);

    let s = get_a_str(&n);
    println!("s = {}", s);
}