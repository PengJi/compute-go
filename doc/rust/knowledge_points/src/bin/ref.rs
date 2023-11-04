// 引用

fn give_ownership() -> String {
    let s = String::from("hello");
    s
}

fn take_and_give_ownership(s: String) -> String {
    s
}

// 所有权转移
fn test_ownership() {
    let s1 = give_ownership();
    println!("s1 = {}", s1);

    let mut s2 = String::from("hello");
    let s3 = takes_and_gives_back(s2);
    s2 = takes_and_gives_back(s3);  // 可以使用引用优化
    println!("s2 = {}", s2);
}

// 引用: &,
// 创建一个指向值的应用，但是并不拥有它，因为不拥有这个值,
// 所以，当引用离开其值指向的作用域后也不会被丢弃。
//
// 借用: &mut

// 引用，没有发生所有权转移
fn calculate_len(s: &String) -> usize { s.len() }

// 借用
fn modify_s(s: &mut String) { s.push_str(", world"); }

fn test_ref() {
    let mut s1 = String:from("hello");

    // 引用
    let s= &s1;
    let len = calculate_len(s);
    println!("len = {}", len);

    // 借用
    let ms = &mut s1;
    modify_s(&ms);

    // println!("s1 = {}", s1); // error，已经借用了，所以这里不可访问
    // println!("s = {}", s);  // error，已经借用了，所以这里不可访问
    println!("ms = {}", ms);
}

fn test_ref1() {
    let mut s1 = String::from("hello");

    let r1 = &s1;
    let r2 = &s1;
    println!("{}, {}", r1, r2);

    let r3 = &mut s1;
    r3.push_str(", world");
    // println!("{}, {}", r1, r2);  // error, 已被借用
}

fn main() {
    test_ownership();
    test_ref();
    test_ref1();
}
