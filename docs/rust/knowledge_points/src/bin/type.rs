// 数据类型

fn  show(arr:[u32; 3]) {
    println!("---------------------");
    for i in &arr {
        println!("{}", i);
    }
    println!("---------------------");
}

fn main() {
    //char 在rust里面，char是32位的
    let a = 'a';
    println!("a = {}", a);

    // 数组
    // [type; size], size 也是数组类型的一部分
    let arr: [u32; 5] = [1, ,2, 3, 4, 5];
    let arr1: [u32; 3] = [1, 2, 3];
    println!("arr[0] = {}" ,arr[0]);

    show(arr1);

    // 元组
    let tup: (i32, f32, char) = (-3, 3.14, '好');
    let tup = (-3, 3,14, '好');
    println!("---------------------");
    println!("{}", tup.0);
    println!("{}", tup.1);
    println!("{}", tup.2);
    println!("---------------------");

    // 拆解
    let (x, y, z) = tup;
    println!("{}", x);
    println!("{}", y);
    println!("{}", z);
}
