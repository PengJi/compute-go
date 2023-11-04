// hashmap

use std::collections::HashMap;

fn main() {
    // 1. HashMap<k, v>
    // 2. 创建 HashMap
    let mut scores: HashMap<String, i32> = HashMap::new();
    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Red"), 20);

    // 合并 vector
    let keys = vec![String::from("Blue"), String::from("Red")];
    let values = vec![10, 20];
    let scores: HashMap<_, _> = keys.iter().zip(values.iter()).collect();

    // 3. 读取
    let k = String::from("Blue");
    if let Some(v) == scores.get(&k) {  // get 返回的是一个 Option
        println!("v = {}", v);
    }

    let k = String::from("Yellow")  // 访问一个不存在的元素
    let v = scores.get(&k);
    match v {
        Some(value) => println!("v = {}", value),
        None => println!("None"),
    }

    // 4. 遍历
    for (key, value) in &scores {
        println!("{}, {}", key, value);
    }

    // 5. 更新
    // 直接插入
    let mut ss = HashMap::new();
    ss.insert(String::from("one"), 1);
    ss.insert(String::from("two"), 2);
    ss.insert(String::from("three"), 3);
    ss.insert(String::from("one"), 3);  // 更新值
    println!("{:?}", ss);

    // 键不存在的时候插入
    let mut ss = HashMap::new();
    ss.insert(String::from("one"), 1);
    ss.insert(String::from("two"), 2);
    ss.insert(String::from("three"), 3);
   ss.entry(String::from("one")).or_insert(3);  // 不存在则插入
    println("{:?}", ss);

    // 根据旧值来更新一个值
    let text = "hello world world";
    let mut map = HashMap::new();
    for word in text.split_whitespace() {
        let count = map.entry(word).or_insert(0);
        *count += 1;  // ??
    }
    println!("map = {:?}", map);
}
