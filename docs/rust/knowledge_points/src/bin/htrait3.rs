// 完全限定语法
//定义：<Type as Trait>::function(.....)

// trait A {
//     fn print(&self);
// }

// trait B {
//     fn print(&self);
// }

// struct MyType;

// impl A for MyType {
//     fn print(&self) {
//         println!("A trait for MyType");
//     }
// }

// impl B for MyType {
//    fn print(&self) {
//        println!("B trait for MyType");
//    }
// }

// impl MyType {
//    fn print(&self) {
//        println!("MyType");
//    }
// }

// fn main() {
//    let my_type = MyType;
//    my_type.print();  // 等价于MyType::print(&my_type);

//    A::print(&my_type);
//    B::print(&my_type);
// }

trait Animal {
    fn name() -> String;
}

struct Dog;

impl Dog {
    fn name() -> String {
        String::from("Spot")
    }
}

impl Animal for Dog {
    fn name() -> String {
        String::from("puppy")
    }
}

fn main() {
    println!("name: {}", Dog::name());
    // println!("name: {}", Animal::name());  // error    
    println!("name: {}", <Dog as Animal>::name());  // 完全限定语法
}
