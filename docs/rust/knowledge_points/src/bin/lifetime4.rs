// 方法中的生命周期

struct StuA<'a> {
    name: &'a str,
}

impl<'b> StuA<'b> {
    fn do_something(&self) -> i32 {
        3
    }

    fn do_something2(&self, s: &str) -> &str {
    // 相当于下面显示的声明生命周期
    // fn do_something2<'b>(&'b self, s: &str) -> &'b str {
        self.name
    }

    // 如果不指定生命周期，则会报错，因为编译器会默认当成如下格式：
    // fn do_something2<'b>(&'b self, s: &str) -> &'b str {
    fn do_something3<'a>(&self, s: &'a str) -> &'a str {
        s
    }
}

fn main() {
    let s = String::from("hello");
    let a = StuA{name: &s};
    println!("{}", a.do_something);

    let s2 = String::from("world");
    println!("{}", a.do_something2(&s2));

    println!("{}", a.do_something3(&s2));
}
