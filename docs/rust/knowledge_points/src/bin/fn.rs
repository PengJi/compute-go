// 函数

// 不返回值
fn test_fun() {
    println!("This is s function");
}

// 带参数和返回值的函数
fn test_fun1(a: i32, b: i32) -> i32 {
    let res = a + b;
    return res;
}

fn test_fun2(a: i32, b: i32) -> i32 {
    // let resutl = a + b;
    // result
    // 或
    a + b
}

fn main() {
    test_fun();

    let a: i32 = 9;
    let b: i32 = 10;
    test_fun1(a, b);

    let r: i32 = test_fun2(a, b);
    println!("r = {}", r);

    // 语句是执行一些操作，但是不返回值的指令
    // let y = 1; // 语句，不返回值
    // let x = (let y = 1)

    // 表达式会计算一些值
    let y = {
        let x = 1;
        // x + 1; // 错误
        x + 1
    };
}
