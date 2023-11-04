
查看支持哪些 OS 和 CPU 架构
`rustc --print target-list | pr -tw100 --columns 3`

查看安装的 toolchains 和 target
`rustup show`

toolchain 是交叉编译所需的"编译工具"，target 则是编译到目标平台所需的"库文件"。
比如 Ubuntu 默认的 target 是 gnu 的，依赖 glibc，但是其他 Linux 系统未必是 glibc 是基础库，但是可以用同一套 toolchain（编译器之类的），因此只需要添加 target 即可。
而交叉编译到 Windows，则 Linux 的编译器是没有这个能力的，因此需要添加 Windows 平台的 toolchain（有部分tool官方没有实现还得添加第三方的tool），然后再添加 target。
注意，如果 Windows 选择的是 msvc 而非 gnu，那么哪怕是最简单的 hello world 也必须要安装 visual studio（主要是需要它携带的toolchain【linker等】）。
使用 ldd 命令可以查看程序依赖的动态库。

`rustup target add x86_64-unknown-linux-musl`（可以加 --toolchain=stable，但是默认是stable，也可以安装nightly的）【可以用 `rustup show`查看安装了哪些工具链，可以看到 `stable-x86_64-unknown-linux-gnu` 是默认的工具链】
【注意，目前PC的话大多处理器架构都是x86_64的，如果目标运行机器不是这个架构的需要做出调整，Linux可以通过 `arch` 命令查看处理器架构，Windows通过 `systeminfo` 查看，x86_64,x64,AMD64 是同一个架构】


# 在 Linux 下编译 Windows 程序
1. `rustup toolchain install stable-x86_64-pc-windows-gnu`  
2. `rustup target add x86_64-pc-windows-gnu --toolchain=stable`
3. 安装 linker `mingw-w64`
4. 修改 ~/.cargo/config
```toml
[target.x86_64-pc-windows-gnu]
linker = "/usr/bin/x86_64-w64-mingw32-gcc"
ar = "/usr/bin/x86_64-w64-mingw32-ar"
```
5. `cargo build --release --target=x86_64-pc-windows-gnu`
然后在target目录里有x86_64-pc-windows-gnu目录里有release目录可以找到对应可执行文件。
x86_64-pc-windows-gnu 的程序用 ldd 查看也是不依赖动态库的；

# 在 Linux 编译 Linux 平台的程序
1. `rustup target add x86_64-unknown-linux-musl`
2. `cargo build --release --target=x86_64-unknown-linux-musl`
使用 ldd 查看生成的程序是否依赖动态库，预期是没有任何依赖。


# 参考
[Cross-compilation in Rust](https://kerkour.com/rust-cross-compilation)
[japaric/rust-cross](https://github.com/japaric/rust-cross#cross-compiling-with-cargo)
[Foreign Function Interface](https://doc.rust-lang.org/nomicon/ffi.html)
