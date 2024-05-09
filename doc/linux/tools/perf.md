# 使用 perf state
```bash
# 监控整个系统的性能事件，包括 CPU 周期数、指令数等
perf stat -a

# 监控特定进程
perf stat -p 12345

# 监控特定事件
# 监控特定的性能计数器，如 CPU 周期数、执行的指令数和缓存未命中数，针对进程 ID 为 12345 的进程。
perf stat -e cycles,instructions,cache-misses -p 12345
```

# 使用 perf record
```bash
# 监控特定进程
sudo perf record -g -F 99 -p 4142

# 查看报告
sudo perf report -g -i perf.data
```


# 火焰图
```bash
git clone https://github.com/brendangregg/FlameGraph.git
perf script -i perf.data > out.perf
FlameGraph/stackcollapse-perf.pl out.perf > out.floded
FlameGraph/flamegraph.pl out.floded > cp.svg
```
1. 火焰图中的每一个方框是一个函数，方框的宽度代表了它的执行时间，所以越宽的函数，执行越久。  
2. 火焰图的楼层每高一层，就是更深一级的函数被调用，最顶层的函数，是叶子函数。
3. 火焰图是基于 stack 信息生成的 SVG 图片, 用来展示 CPU 的调用栈。
4. y 轴表示调用栈, 每一层都是一个函数. 调用栈越深, 火焰就越高, 顶部就是正在执行的函数, 下方都是它的父函数.
5. x 轴表示抽样数, 如果一个函数在 x 轴占据的宽度越宽, 就表示它被抽到的次数多, 即执行的时间长. 注意, x 轴不代表时间, 而是所有的调用栈合并后, 按字母顺序排列的
