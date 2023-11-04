## 介绍
Rust 由 Graydon Hoare 在 2008 年私人研发，2009年得到 Mozilla 赞助，2010 年首次发布 0.1.0 版本，用于 Servo 引擎的研发。2015年5月15号 年 Rust 发布 1.0 版本。2021年2⽉9号，Rust 基⾦会宣布成⽴，以致⼒于在全球范围内推⼴和发展 Rust 语⾔。
* 2015-2018 工具、文档、编译器更加智能  
* 2018-2021 异步生态完善  

一门赋予每个人构建可靠且高效软件能力的语言，Rust 原则：
* 可靠性（Realiable）如果它能够编译，它就可以工作。
* 高性能（performant）既高效执行又使用最少内存。
* 生产力（Porductive）让工作事半功倍。
* 便捷性（Supportive）语言、工具和社区随时为用户提供帮助。
* 透明性（Transparent）让用户可以预测和控制底层细节。
* 多样性（Versatile）用 Rust 做任何事。

总的来说，Rust 有三大优势：
1. ⾼性能，Rust 执行速度快且内存利用率高，没有运行时和垃圾回收，能够用于对性能要求高的服务，且可以在嵌入式设备商运行，还能轻松与其他语言集成。
2. 可靠性，Rust 保证了内存安全和线程安全，在编译时就能够避免大多数运行时可能发生的错误。
3. 生产力，Rust 拥有出色的文档、强大的编译器和清晰的错误提示，还提供了方便的包管理工具和构建工具。

## Rust 学习

### 基础知识点
**通用编程概念**  **所有权**  **结构体**  **枚举与模式匹配**
**vector, string, hashmap**  **包，crate, 模块**
**测试**

### 进阶知识点
**错误处理**  **泛型**  **trait**  **生命周期**
**迭代器**  **闭包**  **只能指针**  **线程**  **面向对象**
**高级特征**

[Rust 学习资料汇总](https://github.com/rcore-os/rCore/wiki/study-resource-of-system-programming-in-RUST)
[The Rust Programming Language](https://doc.rust-lang.org/book/)  
[The Rust Programming Language source code](https://nostarch.com/Rust2018)   
[Rust By Example](https://doc.rust-lang.org/rust-by-example/)  
[Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)  
[The Rustonomicon](https://doc.rust-lang.org/nomicon/)   
[The Cargo Book](https://doc.rust-lang.org/cargo/guide/)  
[Rust 过程宏开发实战](https://space.bilibili.com/500416539/channel/collectiondetail?sid=34404)  

### 原理
1. async 原理；
2. 手写链表；
3. 智能指针区别；

***

## 安装
安装 Rust 版本管理器 rustup 和 Rust 包管理器 cargo
```sh
curl https://sh.rustup.rs -sSf | sh
···

如果下载官方脚本较慢，则可修改 rustup 的镜像地址
中国科学技术大学镜像服务器
```sh
export RUSTUP_DIST_SERVER=https://mirrors.ustc.edu.cn/rust-static
export RUSTUP_UPDATE_ROOT=https://mirrors.ustc.edu.cn/rust-static/rustup
curl https://sh.rustup.rs -sSf | sh
```

或换成清华大学镜像源
```sh
export RUSTUP_DIST_SERVER=https://mirrors.tuna.edu.cn/rustup
export RUSTUP_UPDATE_ROOT=https://mirrors.tuna.edu.cn/rustup/rustup
curl https://sh.rustup.rs -sSf | sh
```

使生效
```sh
source $HOME/.cargo/env
# 查看版本
rustc --version
```
 
安装 rustc 的 nightly 版本，并把该版本设置为 rustc 的缺省版本。
```sh
rustup install nightly
rustup default nightly
```

把软件包管理器 cargo 所用的软件包镜像地址 crates.io 换成 tuna 源来加速三方库的下载。
打开或新建 `~/.cargo/config` 文件
```sh
[source.crates-io]
replace-with = 'tuna'

[source.tuna]
registry = "https://mirrors.tuna.tsinghua.edu.cn/git/crates.io-index.git"
```

## 更新
rustup update

## 卸载
rustup self uninstall

## 显示版本
rustc --version

## cargo 使用
新建项目：`cargo new hello`  
只编译检查，不生成可执行文件：`cargo check`  
调试模式构建：`cargo build`  
发布模式构建：`cargo build --release`  
创建 lib：`cargo new --lib mylib`  
运行：`cargo run`  
打印堆栈：`RUST_BACKTRACE=1 cargo run`  
生成文档（在浏览器中打开当前项目用到的库的文件）：`cargo doc --open`

***

# 其他
[了解下Rust 模块使用方式](https://juejin.cn/post/7070481262749679653#heading-5)
