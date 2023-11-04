// 泛型和 trait 使用
// 类型 T 必须实现了 PartialOrd 和 Copy
//fn largest<T: PartialOrd + Copy> (list: &[T]) -> T {  // 或
fn largest<T> (list: &[T]) -> T
    where T: PartialOrd + Copy
{
    let mut larger = list[0];
    for &item in larger.iter() {
        if item > larger {
            larger = item;
        }
    }

    larger
}

fn main() {
    let number_list = vec![1, 23, 33, 6, 10];
    let max_number = largest(&number_list);
    println!("max_number: {}", max_number);

    let char_list = vec!['a', 'd', 'b'];
    let max_char = largest(&char_list);
    println!("max_char: {}", max_char);
}
