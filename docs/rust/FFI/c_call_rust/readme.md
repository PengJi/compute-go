C 语言调用 rust
1. `cargo new foo --lib`
2. `cd foo`
3. `cargo build`  # 生成静态库，注意要修改 toml
4. `cp target/debug/libfoo.a ../`
5. `cd ..`
6. `gcc -o main main.c libfoo.a` 或者 `gcc -o main main.c libfoo.a -lpthread -ldl`
7. `./main`
