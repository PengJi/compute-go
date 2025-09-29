// 1. trait bound（对类型的约束） 的写法
// fn print_information(item: impl GetInformation) {}  // 直接作为参数的写法
// fn print_information<T: GetInformation>(item: T) {  // 使用 trait bound 的写法
//     println!("name = {}", item.name);
//     println!("age = {}", item.age);
// }

// 2. 指定多个 trait bound
trait GetName {
    fn get_name(&self) -> &String;
}

trait GetAge {
    fn get_age(&self) -> u32;
}

// 写法一
// 使用 trait bound 的写法
// 尖括号里面的是泛型T，后面是对 T 的约束，参数 item 的类型为 T
fn print_information<T: GetName+GetAge> (item: T) {
    println!("name = {}", item.get_name());
    println!("age = {}", item.get_age());
}

// 写法二
// 防止在尖括号里面的约束太长
fn print_information<T>(item: T)
    where T: GetName+GetAge
{
    println!("name = {}", item.get_name());
    println!("age = {}", item.get_age());
}

pub struct Student {
    pub name: String,
    pub age: u32,
}

impl GetName for Student {
    fn get_name(&self) -> &String {
        &self.name
    }
}

impl GetAge for Student {
    fn get_age(&self) -> u32 {
        &self.age
    }
}

// 3. 返回值为 trait
// 当 trait 作为返回值，要求返回的对象实现 GetAge
fn produce_item_with_age() -> impl GetAge {
    Student {
        name: Stirng::from("xiaoming"),
        age: 20,
    }
}

pub struct Teacher {
    pub name: String,
    pub age: u32,
}

impl GetAge for Teacher {
    fn get_age(&self) -> u32 {
        self.age
    }
}

// 错误的用法
// 必须返回同一种类型，尽管 Teaher 实现了同样的 trait，这里也会报错，必须是一个类型 
// fn produce_item_with_age_error() -> impl GetAge {
//     let is = true;
//     if is {
//         Student {
//             name: Stirng::from("xiaoming"),
//             age: 15,
//         }
//     } else {
//         Teacher {
//             name: String::from("xiaoliang"),
//             age: 20,
//         }
//     }
// }

fn main() {
    let s = Student(name: "xiaoming".to_string(), age: 10);
    print_information(s);

    let s = produce_item_with_age();
}
