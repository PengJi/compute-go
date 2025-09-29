// 函数指针
// 函数指针允许我们使用函数所有一个函数的参数。
// 函数的类型是 fn，fn 被称为函数指针，指定参数为函数指针的语法类似于闭包
// 函数指针都实现了 Fn、FnMut、FnOnce

fn add_one(x: i32) -> i32 {
    x + 1
}

fn do_twice(f: fn(i32)->i32, val: i32) -> i32 {
    f(val) + f(val)
}

fn wrapper_func<T>(t: T, v: i32) -> i32
    where T: Fn(i32) -> i32 {  // 参数必须实现 Fn trait
    t(v)
}

fn func(v: i32) -> i32 {
    v + 1
}

fn main() {
    let r = do_twice(add_one, 5);  // 传入函数指针
    println!("r = {}", r);
    
    let a = wrapper_func(|x| x+1, 1);  // 使用闭包
    println!("a = {}", a);

    let b = wrapper_func(func, 1);  // 传入函数指针
    println!("b = {}", b);
}
