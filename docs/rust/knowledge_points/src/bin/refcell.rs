// 内部可变性：允许在使用不可变引用时改变数据。
//
// RefCell<T> 在运行时检查借用规则（通常情况下在编译时检查借用规则）。
// RefCell<T> 代表数据的唯一所有权，只呢该用于单线程场景。
// 
// Box<T> Rc<T> RefCell<T> 不同：
// RC<T> 允许相同数据有多个所有者，Box<T> 和 RefCell<T> 有单一所有者。
// Box<T> 允许在编译时执行不可变或可变借用检查，Rc<T> 仅允许在编译时执行不可变借用检查，
// RefCell<T> 允许在执行时不可变或可变借用检查。
// 由于 RefCell<T> 允许在执行时执行可变借用检查，所有我们可以再即便 RefCell<T> 自身是不可变的情况下修改其内部的值。

#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    let value = Rc::new(RefCell::new(5));
    
    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));
    let b = Cons(Rc::new(RefCell::new(6)), Rc::new(&a));
    let b = Cons(Rc::new(RefCell::new(7)), Rc::new(&a));

    println!("a before: {:?}", a);
    println!("a before: {:?}", b);
    println!("a before: {:?}", c);

    *value.borrow_mut() += 10;
    println!("a after: {:?}", a);   
    println!("a after: {:?}", b);   
    println!("a after: {:?}", c);   
}
