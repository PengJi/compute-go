extern crate crypto;

use crypto::digest::Digest;
use crypto::sha3::Sha3;

// use mylib::factory::produce_refrigerator;
// use mylib::factory::produce_refrigerator::produce_re;
// use mylib::factory::produce_washing_machine;
// use mylib::factory::produce_washing_machine as A;

use mylib::factory::*;

mod modA {
    #[derive(Debug)]
    pub struct A {  // 模块内结构体
        pub number: i32,
        name: String,
    }

    impl A {
        pub fn new_a() -> A {
            A {
                number: 1,
                name: String::from("A"),
            }
        }

        pub fn print_a(&self) {
            println!("number: {}, name: {}", self.number, self.name);
        }
    }

    pub mod modB {
        pub fn print_B() {
            println!("B");
        }

        pub mod modC {
            pub fn print_C() {
                println!("C");
                super::print_B();  // 调用父类的方法
            }
        }
    }
}

// use modA::A;
use modA::A as A1;

fn main() {
    println!("===========use mod from lib============");
    mylib::factory::produce_refrigerator::produce_re();  // 绝对路径
    produce_refrigerator::produce_re();  // 相对路径
    produce_washing_machine::produce_re();  // 相对路径
    // A::produce_re();

    println!("===========use mod==============");
    //let a = modA::A::new_a();  // 绝对路径
    //let a = A::new_a();  // 相对路径
    let a = A1::new_a();
    a.print_a();

    let number = a.number;  // public
    //let name = a.name;  // error, private

    modA::modB::modC::print_C();

    println!("============ use extern crate============");
    let mut hasher = Sha3::sha3_256();
    hasher.input_str("hello world");
    let result = hasher.result_str();
    println!("hash = {}", result);

    println!("============= error =================");
    

    println!("hello world");
}
