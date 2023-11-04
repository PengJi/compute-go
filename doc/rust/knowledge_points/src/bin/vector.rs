// vector

fn main() {
    // 1. 创建空的 vector: Vec<T>
    let mut v: Vec<i32> = Vec::new();
    // v.push(1);

    // 2. 创建包含初始值的 vector
    let v = vec![1, 2, 3];  // 使用宏

    // 3. 丢弃 vector
    {
        let v1 = vec![1, 2, 3];
    }

    // 4. 读取元素
    let one: &i32 = &v[0];
    // let four: &i32 = &v[3];
    println!("one = {}", one);
    println!("one = {}", *one);

    // 推荐的方法
    // match v.get(1) {
    match v.get(3) {
        Some(value) => println!("value = {}", value),
        _ => println!("None"),
    }

    // 5. 更新
    let mut v2: Vec<i32> = Vec::new();
    v2.push(1);
    v2.push(2);
    v2.push(3);

    // 6. 遍历
    // （1）不可变遍历
    for i in &v2 {
        println!("i = {}", i);
    }
    // （2）可变的便利
    for i in &mut v2 {
        *i += 1;
        println!("i = {}", i);
    }

    // 7. 使用枚举
    enum Context {
        Text(String),
        Float(f32),
        Int(i32),
    };
    let c = vec![
        Context::Text(String::from("string")),
        Context::Int(-1),
        Context::Float(0.01), 
    ];

    // 注意事项
    let mut v = vec![1, 2, 3, 4, 5];
    let first = &v[0];  // 不可变引用
    v.push(6);  // 已修改
    // println!("first = {}", first);  // error, 不可变引用之后又修改
}
