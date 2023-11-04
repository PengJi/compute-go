// 函数中的生命周期
// 指定函数返回值的生命周期依赖于相关参数的生命周期
// 函数或者方法的参数的生命周期称为输入生命周期，而返回值的生命周期为输出生命周期

// fn longer(x: &str, y: &str) -> &str {  // missing lifetime
fn longer<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

fn get_str<'a>(x: &'a str, y: &str) -> &'a str {
    x
}

// error
// fn a_str<'a>(x: &'a str, y: &'a str) -> &'a str {
//     let r = String::from("abc");
//     r.as_str()  // 返回局部变量的引用
// }
    
fn main() {
    let s1 = String::from("abcde");
    let s2= String::from("ab");
    let r = longer(s1.as_str(), s2.as_str());
    println!("r = {}", r);

    let ss = get_str(s1.as_str(), s2.as_str());
    // let ss2 = a_str(s1.as_str(), s2.as_str());
}
