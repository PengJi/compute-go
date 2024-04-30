编译 glib 程序
```cpp
gcc demo.c -o demo $(pkg-config --cflags --libs glib-2.0)
```
