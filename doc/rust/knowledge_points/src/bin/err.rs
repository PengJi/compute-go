// 错误处理

// rust语言将错误分为两个类别：可恢复错误和不可恢复错误
//（1）可恢复错误通常代表向用户报告错误和重试操作是合理的情况，例如未找到文件。rust中使用Result<T,E>来实现。
//（2）不可恢复错误是bug的同义词，如尝试访问超过数组结尾的位置，rust中通过panic！来实现。
//
// 当编写一个函数，但是该函数可能会失败，此时除了在函数中处理错误外，还可以将错误传给调用者，让调用者决定如何处理，这被称为传播错误。
//
// 什么时候用 panic！，什么时候用 Result
// (1)示例、代码原型、测试用 panic!\unwrap\expect
// (2)实际项目中应该用Result
//
// Option和Result

use std:fs::File;

fn test_err1() {
    //Result<T, E>
    //enum Result<T, E> {
    //  Ok(T),
    //  Err(E),
    //}
    // let f = File::open("hello.txt");
    // let r = match r {
    //     Ok(file) => file,
    //     Err(error) => panic!("error: {:?}", error)
    // };

    // let f = File::open("hello.txt").unwrap();  // 简写方式
    let f = File::open("hello.txt").expect("Failed to open file");  // 自定义错误信息

    // panic!("panic here");
}

use std::io;
use std::io::Read;
use std::fs::File;

//fn read_username_from_file() -> Result<String, io::Error> {
//    let f = File::open("hello.txt");
//    let mut f = match f {
//        Ok(file) => file,
//        Err(error) => return Err(error),
//    };
//
//    let mut s = String::new();
//    match f.read_to_string(&mut s) {
//        Ok(_) => Ok(s),
//        Err(error) => Err(error),
//    }
//}
//
// 传播错误的简写方式，提倡的方式
//fn read_username_from_file() -> Result<String, io::Error> {
//    let mut f = File::open("hello.txt")?;
//
//    let mut s = String::new();
//    f.read_to_string(&mut s)?;
//    Ok(s)
//}
// 
// 更进一步的简写
fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new();
    File::open("hello.txt")?.read_to_string(&mut s)?;
    Ok(s)
}

fn test_err2() {
    let r = read_username_from_file();
    match r {
        Ok(s) => println!("s = {}", s),
        Err(e) => println!("err = {:?}", e),
    }

}

fn main() {
    test_err1();
    test_err2();
}
