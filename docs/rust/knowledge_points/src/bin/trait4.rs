// 使用 trait bound 有条件的实现方法

trait GetName {
    fn get_name(&self) -> &String;
}

trait GetAge {
    fn get_age(&self) -> u32;
}

struct PeopleMatchInfo<T, U> {
    master: T,
    student: U,
}

impl<T: GetName+GetAge, U: GetName+GetAge> PeopleMatchInfo<T, U> {
    fn print_all_information(&self) {
        println!("master name = {}", self.master.get_name());
        println!("master age = {}", self.master.get_age());
        println!("student name = {}", self.student.get_name());
        println!("student age = {}", self.student.get_age());
    }
}

struct Teacher {
    name: String,
    age: u32,
}

impl GetName for Teacher {
    fn get_name(&self) -> &String {
        &self.name
    }
}

impl GetAge for Teacher {
    fn get_age(&self) -> &u32 {
        self.age
    }
}

struct Student {
    name: String,
    age: u32,
}

impl GetName for Student {
    fn get_name(&self) -> &String {
        &self.name
    }
}

impl GetAge for Student {
    fn get_age(&self) -> u32 {
        self.age
    }
}

fn main() {
    let s = Student{name: "xiaoming".to_string(), age: 20};
    let t = Teacher{name: "xiaoming".to_string(), age: 30};
    let m = PeopleMatchInfo{master: t, student: s};
    m.print_all_information();
}
