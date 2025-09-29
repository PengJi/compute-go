// 结构体

#[drive(Debug)]  // 打印结构体

fn test_struct() {
    // 1. 定义结构体
    struct User {
        name: String,
        count: u64,
        active: bool,
    }

    // 2、 创建结构体实例
    let xiaoming = User {
        name: String::from("xiaoming"),
        count: 10000,
        active: true,
    }

    // 打印结构体
    println!("xiaoming: {:?}", xiaoming);
    println!("xiaoming: {:#?}", xiaoming);

    // 3. 修改结构体
    let mut xiaohuang = User {
        name: String::from("xiaohuang"),
        count: 100000,
        active: true,
    }
    xiaohuang.count = 20000;

    // 4. 参数名字和字段名字相同的简写方法
    let name = String::from("zhangsan");
    let count = 30000;
    let active = true;

    let user1 = User {
        name,
        count,
        active,
    }

    // 5. 从其他结构体创建实例
    let user2 = User {
        name: String::from("lisi"),
        ..user1
    }
    println!("name = {}", user2.name);
    println!("count = {}", user2.count);

    // 6. 结构体元组
    // 特征：字段没有名字；圆括号
    struct Point(i32, i32);
    let a = Point(10, 20);
    let b = Point(30, 40);
    println!("a.x = {}, a.y = {}", a.0, a.1);

    // 7. 没有任何字段的类单元结构体
    struct A{};
}

struct Dog {
    name: String,
    weight: f32,
    height: f32,
}

// 方法
impl Dog {
    fn get_name(&self) -> &str {
        &(self.name[..])
    }

    fn get_weight(&self) -> &f32 {
        self.weight
    }

    // fn get_height(&self) -> f32 {
    //     self.height
    // }

    fn show() {
        println!("bark bark bark");
    }
}

impl Dog {
    fn get_height(&self) -> f32 {
        self.height
    }
}

fn test_impl() {
    let dog = Dog {
        name: String::from("wangwang"),
        weight: 90.0,
        height: 70.5,
    }

    println!("dog: {:#?}", dog);
    println!("name: {}", dog.get_name());
    println!("weight: {}", dog.get_weight());
    println!("height: {}", dog.get_height());

    Dog::show();
}


fn main() {
    test_struct();
    test_impl();
}
