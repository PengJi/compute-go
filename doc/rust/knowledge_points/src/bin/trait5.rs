// 对任何实现了特定 trait 的类型有条件的实现 trait

trait GetName {
    fn get_name(&self) -> &String;
}

trait PrintName {
    fn print_name(&self);
}

// 如果泛型 T 实现了 GetName，则可实现 PrintName
// 泛型 T 必须实现 trait GetName
impl<T: GetName> PrintName for T {
    fn print_name(&self) {
        println!("{}", self.get_name());
    }
}

struct Student {
    name: String,
}

// 实现了 GetName 的 trait，则具有了 PrintName 的 trait
impl GetName for Student {
    fn get_name(&self) -> &String {
        &(self.name)
    }
}

fn main() {
    let s = Student{name: String::from("xiaoming")};
    s.print_name();
}
