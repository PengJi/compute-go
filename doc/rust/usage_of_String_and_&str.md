首先来看一段代码：
```rust
fn main() {
    let my_name = "Pascal";
    greet(my_name);
}

fn greet(name: String) {
    println!("Hello, {}!", name);
}
```

运行上面的代码会产生如下的报错：
```rust
error[E0308]: mismatched types
 --> src/main.rs:3:11
  |
3 |     greet(my_name);
  |     ----- ^^^^^^^- help: try using a conversion method: `.to_string()`
  |     |     |
  |     |     expected struct `String`, found `&str`
  |     arguments to this function are incorrect
  |
note: function defined here
 --> src/main.rs:6:6
  |
6 |   fn greet(name: String) {
  |      ^^^^^ ------------

For more information about this error, try `rustc --explain E0308`.
```
编译器清楚的告诉了我们存在的问题及修改方法。greet 期望传入 String 类型的值，但我插入的值为 &str。修改方法为使用类型转换函数 to_string，即 my_name.to_string()。
接下来，我们具体分析一下原因。

# 理解 String 类型
我们先看一下 my_name 在内存中是如何存储的，假设这里已执行 to_string()，即将 my_name 转为了 String 类型。
```
                     buffer
                   /   capacity
                 /   /  length
               /   /   /
            +–––+–––+–––+
stack frame │ • │ 8 │ 6 │ <- my_name: String
            +–│–+–––+–––+
              │
            [–│–––––––– capacity –––––––––––]
              │
            +–V–+–––+–––+–––+–––+–––+–––+–––+
       heap │ P │ a │ s │ c │ a │ l │   │   │
            +–––+–––+–––+–––+–––+–––+–––+–––+

            [––––––– length ––––––––]
```
Rust 会在栈上存储 String 对象，这个对象包含：一个指针指向一块在堆上分配的缓存（buffer），缓存中存放着真正的数据；缓存的容量大小；数据的长度。这里 String 对象是固定三个字长的大小。
String 能够根据需要调整缓存的容量。例如可以使用 `push_str()` 追加更多的字符（String 对象必须是 mut），这种追加操作可能会引起缓存容量的增长。
```rust
let mut my_name = "Pascal".to_string();
my_name.push_str( " Precht");
```
String 的这种行为类似 `Vec<T>`，它们的特征和行为本质上是相同的，只不过 String 是 utf-8 编码的。

# 理解字符串切片（string slices）
当我们引用一个 utf-8 字符串（被其他变量拥有）的一个区间，或者使用字符串字面量（string literals），我们就需要使用字符串切片（str）。

如果我们只想获取 last name，我们像下面这样可以只引用 my_name 的一部分。
```rust
let mut my_name = "Pascal".to_string();
my_name.push_str( " Precht");

let last_name = &my_name[7..];
```
通过指定 从 my_name 的第7个字节一直到缓存区的末尾("..")，last_name 是一个引用自 my_name 所拥有的字符串的字符串切片，即 last_name 借用了 my_name，内存中布局类似如下：
```rust
            my_name: String   last_name: &str
            [––––––––––––]    [–––––––]
            +–––+––––+––––+–––+–––+–––+
stack frame │ • │ 16 │ 13 │   │ • │ 6 │ 
            +–│–+––––+––––+–––+–│–+–––+
              │                 │
              │                 +–––––––––+
              │                           │
              │                           │
              │                         [–│––––––– str –––––––––]
            +–V–+–––+–––+–––+–––+–––+–––+–V–+–––+–––+–––+–––+–––+–––+–––+–––+
       heap │ P │ a │ s │ c │ a │ l │   │ P │ r │ e │ c │ h │ t │   │   │   │
            +–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+–––+
```
last_name 没有在栈上存储容量信息，它只是一个字符串切片的引用，my_name 真正管理位于堆上的字符串。字符串切片（str）是不固定大小的（unsized），并且在实际中，经常通过引用的形式使用，也就是类型为 &str 而不是 str。

# 理解字符串字面量（string literals）
通常在两种情况下使用字符串切片：创建一个子字符串的引用或者使用字符串字面量。
一个字符串字面量通过双引号包含文本创建，如下：
```rust
let my_name = "Pascal Precht"; // This is a `&str` not a `String`
```
这里有一个问题是，如果 &str 是一个引用了被（某人）拥有的 String 的切片，那么这个 String 的所有者是谁？
字符串字面量有点特殊，它们是引用自预分配文本（preallocated text）的字符串切片，这个预分配文本存储在可执行程序的只读内存中。它是装载我们程序的内存并不依赖于堆上分配的缓存区。
也就是说，栈上有一个入口指向程序运行时预分配的内存。
```rust
            my_name: &str
            [–––––––––––]
            +–––+–––+
stack frame │ • │ 6 │ 
            +–│–+–––+
              │                 
              +––+                
                 │
 preallocated  +–V–+–––+–––+–––+–––+–––+
 read-only     │ P │ a │ s │ c │ a │ l │
 memory        +–––+–––+–––+–––+–––+–––+
```

# 应该使用哪一种
这取决于多种因素，但一般地，如果我们的程序不需要拥有或者修改文本（只读），那么应该使用 &str 而不是 String，因此一个合理的改进是：
```rust
fn greet(name: &str) {
    println!("Hello, {}!", name);
}
```

有一种情况，函数参数要求必须是 &str，但由于某些未知原因，String 类型不能转为 &str，rust 也可以处理这种情况。
Rust 有一个特征叫做 deref coercing，这个特征允许把带有借用操作符的 String，即 &String，在函数执行前转成 &str，即 &String 可以当做是 &str。
```rust
fn main() {
    let first_name = "Pascal";
    let last_name = "Precht".to_string();

    greet(first_name);
    greet(&last_name); // `last_name` is passed by reference
}

fn greet(name: &str) {
    println!("Hello, {}!", name);
}
```

# 其他示例

## String 类型与 &str 的特征
```rust
let mut s = String::from("Hello Rust");  // String 类型
println!("{}", s.capacity());    // prints 12
s.push_str("Here I come!");
println!("{}", s.len()); // prints 24

let s = "Hello, Rust!";  // &str 类型
println!("{}", s.capacity()); // compile error: no method named `capacity` found for type `&str`
println!("{}", s.len()); // prints 12
```

## 类型转换

### &str -> String
使用 `to_string()` 或 `String::from()`
```rust
let a = "hello world";  // &str
let c = a.to_string();
let d = a.to_owned();

let b = "OK";
let d = String::from(b);
```

### String -> &str
使用 `&` 或 `as_str()`
```rust
let e = &String::from("Hello Rust");

// 或使用as_str()
let m = String::from("Hello Rust");
let n = m.as_str();

// 不能直接这样使用 
// let e = String::from("Hello Rust").as_str();
```

### String + &str -> String
`String` 后接多个 `&str`
```rust
let mut strs = "Hello".to_string();
// let mut strs = String::from("Hello");
strs.push_str(" Rust");  // " Rust" 是 &str 类型
println!("{}", strs);
```

# 参考
[String vs &str in Rust](https://blog.thoughtram.io/string-vs-str-in-rust/)  
[【翻译】 Rust中的String和&str](https://zhuanlan.zhihu.com/p/123278299)
