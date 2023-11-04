// trait 用于定于与其他类型共享的功能，类似于其他语言中的接口。
// （1）可以通过 trait 以抽象的方式定义共享的行为。
// （2）可以使用 trait bounds 指定泛型是任何拥有特定行为的类型。

// 1. 定义 trait
pub trait GetInformation {
    fn get_name(&self) -> &String;
    fn get_age(&self) -> u32;
}

// 2. 默认实现：可以在定义trait的时候提供默认的行为，trait的类型可以使用默认的行为。
trait SchoolName {
    // 默认方法
    fn get_school_name(&self) -> String {
        String::from("school_name");
    }
}

// 3. 实现 trait
pub struct Student {
    pub name: String,
    pub age: u32,
}

impl SchoolName for Student {}

impl GetInformation for Student {
    fn get_name(&self) -> &String {
        &self.name  // 返回引用
    }

    fn get_age(&self) -> u32 {
        self.age
    }
}

pub struct Teacher {
    pub name: String,
    pub age: u32,
    pub subject: String,
}

impl SchoolName for Teacher {
    fn get_school_name(&self) -> String {  // 这里返回值不能为引用
        String::from("school_name1")  // 注意：如果不是 self，则不能返回引用，否则会造成悬垂指针
    }
}

impl GetInformation for Teacher {
    fn get_name(&self) -> &String {
        &self.name
    }

    fn get_age(&self) -> u32 {
        self.age
    }
}

// 4. trait 作为参数。
// 使用时，item 必须实现 GetInformation 定义的行为
fn print_information(item: impl GetInformation) {
    println!("name = {}", item.get_name());
    println!("age = {}", item.get_age());
}

fn main() {
    let s = Student{name: "xiaoming".to_string(), age: 10};
    let t = Teacher{name: "xiaohuang".to_string(), age: 30, subject: String:from("math")};

    // 定义 trait
    println!("student, name= {}, age = {}", s.get_name(), s.get_age());
    println!("teacher, name= {}, age = {}", t.get_name(), t.get_age());

    // 定义 trait 默认行为
    println!("student school name = {}", s.get_school_name());  // school_name
    println!("teacher school name = {}", t.get_school_name());  // school_name1

    // trait 作为参数
    print_information(s);
    print_information(t);
}
