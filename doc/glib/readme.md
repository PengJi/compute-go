编译 glib 程序
```cpp
gcc test.c -o test $(pkg-config --cflags --libs glib-2.0)
```