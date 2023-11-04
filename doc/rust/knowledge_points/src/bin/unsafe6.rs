// 实现不安全的 trait
// (1) 当至少有一个方法中包含编译器不能验证的不变量时，该 trait 就是不安全的。
// (2) 在 trait 之前增加 unsafe 声明其为不安全的，同时 trait 的实现也必须用 unsafe 标记。

unsafe trait Foo {
    fn foo(&self);
}

struct Bar();

unsafe impl Foo for Bar {
    fn foo(&self) {
        println!("foo");
    }
}

fn main() {
    let a = Bar();
    a.foo();
}
