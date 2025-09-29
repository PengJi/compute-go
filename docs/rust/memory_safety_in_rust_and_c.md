我们编写的程序不可避免地要与内存打交道，关于内存我们要注意两方面的问题：
一 指针要指向有效的内存区域，有效的内存区域是指已分配的并具有正确的类型/大小。如果指向的内存无效，则程序可能会崩溃。
二 内存不会发生泄露。如果分配了一段内存，那么最后一定要被释放。发生内存泄露最终可能耗尽内存。

对于不带 GC 的语言，即像 C/C++ 或者 Rust 这样的底层系统语言，上述问题要么由编译器通过静态分析（C++ RAII，Rust 借用检查器）来保证，要么由程序员来仔细地管理（malloc/free, new/delete）。C语言提供了很少的机制来保护程序免受手动内存管理的危险。

下面通过一个中等复杂的示例来理解在C语言中处理内存时可能出现的问题，并了解现代静态分析工具如何防止此类错误。
本文提供了一个用c编写的专门存储整数的 vector（可调整大小的数组）的实现，它包含至少7个与内存安全的错误，然后我们将它与等价的Rust实现进行比较。
```c
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// There are at least 7 bugs relating to memory on this snippet.
// Find them all!

// Vec is short for "vector", a common term for a resizable array.
// For simplicity, our vector type can only hold ints.
typedef struct {
    int* data;     // Pointer to our array on the heap
    int  length;   // How many elements are in our array
    int  capacity; // How many elements our array can hold
} Vec;

// <bug 1>
// 下面的函数返回一个悬垂指针。
// 该函数返回一个执行该 Vec 的指针，当该函数返回时，指针指向的内容（位于栈上）被释放，所以后续对该指针的使用将会异常。
// 修复的方法是：一使用 malloc(sizeof(Vec)) 将变量内容分配在堆上；二将类型签名更改为返回结构本身，而不是指针。
Vec* vec_new() {
    Vec vec;  // vec 被分配在栈上
    vec.data = NULL;
    vec.length = 0;
    // <bug 2>
    // 初始化容量为0，当调用 vec_push 时，容量将会翻倍但 2*0=0，导致没有额外的内存空间被分配.
    // 因此需要预先分配至少一个元素的空间。
    vec.capacity = 0;
    return &vec;
}

void vec_push(Vec* vec, int n) {
    if (vec->length == vec->capacity) {
        int new_capacity = vec->capacity * 2;
        // <bug 3>
        // malloc 的参数是要分配的内存大小(以字节为单位)。
        // 然而 new_capacity 只是整型的容量。
        // 修复：malloc(sizeof(int) * new_capacity)。
        int* new_data = (int*) malloc(new_capacity);
        assert(new_data != NULL);

        for (int i = 0; i < vec->length; ++i) {
            new_data[i] = vec->data[i];
        }

        // <bug 4>
        // 在 vec->data 调整大小时，没有 free 旧数据指针，将会导致内容泄露。
        vec->data = new_data;
        vec->capacity = new_capacity;
    }

    vec->data[vec->length] = n;
    ++vec->length;
}

// <bug 5>
// free 的顺序不正确。
// 在释放 vector 之后，vec->data 指针就不可用。
// 我们应该先释放 vec->data，然后释放 vector。
void vec_free(Vec* vec) {
    free(vec);
    free(vec->data);
}

void main() {
    Vec* vec = vec_new();
    vec_push(vec, 107);

    // <bug 7>
    // 迭代器 n 失效，这个 bug 不易发现。
    // 首先取一个指向 vector 第一个元素的指针，然而再调用 vec_push 之后，将会发生 resize，
    // 释放旧的数据再分配新的 array。因此 n 是一个悬垂指针，在 printf 中解引用它是内存不安全的。
    // 这是一个称为迭代器失效的常见问题的特殊情况，即当容器被修改时，指向容器的指针将失效。
    int* n = &vec->data[0];
    vec_push(vec, 110);
    printf("%d\n", *n);

    // <bug 6>
    // vec->data 被 free 两次。
    // vec_free 中已经执了一次 free(vec->data)，但这里又被 free 了一次。
    // 修复方式是这里只使用 vec_free。
    free(vec->data);
    vec_free(vec);
}
```
上述程序有 7 个 bug，但这段代码依然可以通过编译（尽管有一些警告），编译后运行该程序将会发生 `Segmentation fault (core dumped)`。
接下来我们使用 rust 实现相同的代码。

```rust
// 使用 Vec2 避免与 std::vec:Vec 冲突。
struct Vec2 {
    data: Box<[isize]>,
    length: usize,
    capacity: usize
}

impl Vec2 {
    fn new() -> &Vec2 {
        let v = Vec2 {
            data: Box::new([]),
            length: 0,
            capacity: 0
        };
        return &v;
    }
}

fn main () {}
```
如果仿照C代码来写 rust，将会编译失败。
```rust
error[E0106]: missing lifetime specifier
 --> src/main.rs:8:17
  |
8 |     fn new() -> &Vec2 {
  |                 ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but there is no value for it to be borrowed from
help: consider using the `'static` lifetime
  |
8 |     fn new() -> &'static Vec2 {
  |                 ~~~~~~~~

For more information about this error, try `rustc --explain E0106`.
```

Rust 可以识别悬垂指针问题，甚至不需要查看函数实现而只需分析函数签名。
上面的错误信息提示：函数的返回了借用的值，但没有值可借用，需要使用 'static 静态生命周期申明。
修复代码：修改函数签名，返回拥有所有权的 vector。
```rust
impl Vec2 {
    fn new() -> Vec2 {
        let v = Vec2 {
            data: Box::new([0]),
            length: 0,
            capacity: 1
        };
        return v;
    }
}
```
需要注意的是，容量问题不会被编译器捕捉到，它是一个逻辑错误，由程序员来识别。
也就是说，如果我们不修复这个 bug，那么错误至少会是一个显式的越界数组错误，而不是访问越界内存的段错误。
接下来，我们实现 push 方法:
```rust
fn push(&mut self, n: isize) {
    if self.length == self.capacity {
        let new_capacity = self.capacity * 2;
        let mut new_data = unsafe {
            let ptr = Heap::default()
                .alloc(Layout::array::<isize>(new_capacity).unwrap())
                .unwrap() as *mut isize;
            Box::from_raw(slice::from_raw_parts_mut(ptr, new_capacity))
        };

        for i in 0..self.length {
            new_data[i] = self.data[i];
        }

        self.data = new_data;
        self.capacity = new_capacity;
    }

    self.data[self.length] = n;
    self.length += 1;
}
```
上述方法可以正确编译和工作，它不包含显式的 `free(self.data)`，因为 rust 会自动释放 `self.data` 的旧值。
实现自动释放是基于 rust 的生命周期，它确定旧数组的生命周期在在变量重新分配时结束。
由于程序员不必显式地释放分配的内存，这消除了相关的内存泄露和两次 free 的问题。

上述的内存分配方式在 rust 中是非惯用的。基本上，内存分配要么通过声明一个值隐式地分配在栈上，
要么使用 Box 或从它派生的任何指针类型显式地分配在堆上。通过这些接口，rust 自动分配适当大小和对齐的内容。
例如：
```rust
struct Point { x: f32, y: f32 }
let p: Box<Point> = Box::new(Point{ x: 0.1, y: 0.2 });
```
Rust 决定 Point 的大小，它会在后台执行 malloc(sizeof(Point))。
tips：在 rust 中分配可变大小数组的规范方法是使用 Vec。

在这里，我们使用不稳定的 hadp 调用内存分配器，它为我们提供了一个指向已分配数据的原始指针 ptr。
Rust 中的原始指针是不受 Rust 编译器管理的内存区域，这意味着 rust 不能确保此类指针的内存安全(防止无效访问)。
然而，rust 提供了获得原始指针所有权的能力，我们使用 `slice::from_raw_parts_mut` 和 `Box::from_raw` 来实现这一点，`Box::from_raw` 告诉 rust 将内存指针视为堆分配数组。
在转移所有权之后，假设内存是有效的并且具有正确的大小/类型，rust 将应用其通常的内存安全检查。

tips：为了执行这些操作，我们必须显式地将代码标记为不安全的。因为如果我们的 rust 程序由于不安全代码的不正确实现而出现段错误，那么只查看相关的不安全代码而不是排查可能跨越整个代码库的错误就会更容易进行调试。

我们不需要实现 vec_free 函数，因为 rust 自动为复合数据结构生成适当的析构函数，即当 Vec2 结构被释放时，rust 知道首先释放 Box<Vec[]>，然后释放 Vec，避免错误的 free 顺序或者 free 两次。最后，如果我们编写 main 函数:
```rust
fn main() {
    let mut vec: Vec2 = Vec2::new();
    vec.push(107);

    let n: &isize = &vec.data[0];
    vec.push(110);
    println!("{}", n);
}
```
编译上面的代码将会出现下面的错误：
```rust
error[E0502]: cannot borrow `vec` as mutable because `vec.data[..]` is also borrowed as immutable
  --> v.rs:50:5
   |
49 |     let n: &isize = &vec.data[0];
   |                      ----------- immutable borrow occurs here
50 |     vec.push(110);
   |     ^^^ mutable borrow occurs here
51 |     println!("{}", n);
52 | }
   | - immutable borrow ends here
```
即使是棘手的迭代器失效错误也会被编译器捕捉到，这是由于其关于借用和可变性的规则。
获取指向 vector 元素的指针将不可变地借用整个 vector，而 push 则需要对 vector 进行可变访问，因此编译器会发现冲突并抛出错误。

总之，rust 帮助我们修复了我们的C实现中与内存相关的每一个错误(除了容量问题，它至少会有更好的错误消息)。记住——这些都是保证，这意味着无论你的代码库有多大，rust 都是强制执行。因为如果我们能把这么多的内存错误加入到50行C语言中，大型代码库的将是一个噩梦。当然，这一切都是以与 rust 的借用检查器作斗争为代价的，包括最初的学习曲线以及围绕它的限制(参见:[Non-lexical lifetimes](http://smallcultfollowing.com/babysteps/blog/2016/04/27/non-lexical-lifetimes-introduction/))进行工作，但对于一个足够大规模的代码库来说，这种痛苦很可能是值得的。


附 rust 完整代码
```rust
#![feature(allocator_api)]

use std::heap::{Heap, Layout, Alloc};
use std::slice;

struct Vec2 {
    data: Box<[isize]>,
    length: usize,
    capacity: usize,
}

impl Vec2 {
    fn new() -> Vec2 {
        let v = Vec2 {
            data: Box::new([0]),
            length: 0,
            capacity: 1,
        };
        return v;
    }

    fn push(&mut self, n: isize) {
        if self.length == self.capacity {
            let new_capacity = self.capacity * 2;
            let mut new_data = unsafe {
                let ptr = Heap::default()
                    .alloc(Layout::array::<isize>(new_capacity).unwrap())
                    .unwrap() as *mut isize;
                Box::from_raw(slice::from_raw_parts_mut(ptr, new_capacity))
            };

            for i in 0..self.length {
                new_data[i] = self.data[i];
            }

            self.data = new_data;
            self.capacity = new_capacity;
        }

        self.data[self.length] = n;
        self.length += 1;
    }
}

fn main() {
    let mut vec: Vec2 = Vec2::new();
    vec.push(107);
    vec.push(110);

    let n: &isize = &vec.data[0];
}
```

[Memory Safety in Rust: A Case Study with C](https://willcrichton.net/notes/rust-memory-safety/)
