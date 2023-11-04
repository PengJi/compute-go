// 闭包、泛型应用
// 实现一个缓存，只处理第一次传入的值并保存

struct Cacher<T> 
    where T: Fn(u32) -> u32  // trait 为一个闭包 
{
    calcuation: T,  // T 要求实现trait Fn，相当与一个回调
    value: Option<u32>,
}

impl<T> Cacher<T>
    where T: Fn(u32) -> u32  // trait bound 
{
    fn new(calcuation: T) -> Cacher<T> {
        Cacher {
            calcuation,
            value: None,
        }
    }

    fn value(&mut self, arg: u32) -> u32 {
        match self.value {
            Some(v) => v,
            None => {
                let v = (self.calcuation)(arg);  // self.calcuation 相当于一个闭包，在以 arg 为参数计 算之后传给 v
                self.value = Some(v);
                v
            }
        }
    }
}

fn main() {
    let mut c = Cacher::new(|x| {x+1});  // 传入一个闭包，效果相当于一个回调
    let v1 = c.value(1);
    println!("v1 = {}", v1);

    let v2 = c.value(2);
    println!("v2 = {}", v2);
}
