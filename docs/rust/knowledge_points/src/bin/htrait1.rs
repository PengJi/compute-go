// 关联类型在 trait 定义中指定占位符类型
// 关联类型是一个将类型占位符与 trait 相关联的方式。
// trait 的实现着会针对特定的实现在这个类型的位置指定相应的具体类型。
// 每个迭代器都实现了 Iterator trait，其定义在标准库中：
// trait Iterator {
//     type Item;
//     fn netxt(&mut self) -> Option<Self::Item>;  // type Item 和 Self::Item 这种用法叫做定义 trait 的关联类型
// }

pub trait Iterator1<T> {
    fn next(&mut self) -> Option<T>; 
}

struct A {
    value: i32,
}

impl Iterator1<i32> for A {
    fn next(&mut self) -> Option<i32> {
        println!("in i32");
        if self.value > 3 {
            self.value += 1;
            Some(self.value)
        } else {
            None
        }
    }
}

impl Iterator1<String> for A {
    fn next(&mut self) -> Option<String> {
        println!("in String");
        if self.value > 3 {
            self.value += 1;
            Some(String::from("hello"))
        } else {
            None
        }
    }
}

fn main() {
    let mut a = A{value: 3};
    // a.next();
    <A as Iterator1<i32>>::next(&mut a);  // 完全限定语法，带上了具体的类型
    <A as Iterator1<String>>::next(&mut a);   
}
