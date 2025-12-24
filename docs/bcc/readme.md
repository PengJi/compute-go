
```bash
查询正在运行的 eBPF 程序
sudo bpftool prog list

导出 eBPF 程序的指令
sudo bpftool prog dump xlated id 89

删除正在运行的 eBPF 程序
sudo bpftool prog delete id {id}

删除正在运行的 eBPF 映射
sudo bpftool map delete id {id}

# 查询当前系统支持的辅助函数列表
bpftool feature probe

# 创建一个哈希表映射，并挂载到/sys/fs/bpf/stats_map(Key和Value的大小都是2字节)
bpftool map create /sys/fs/bpf/stats_map type hash key 2 value 2 entries 8 name stats_map

# 查询系统中的所有映射
bpftool map
#示例输出
#340: hash  name stats_map  flags 0x0
#        key 2B  value 2B  max_entries 8  memlock 4096B

# 向哈希表映射中插入数据
bpftool map update name stats_map key 0xc1 0xc2 value 0xa1 0xa2

# 查询哈希表映射中的所有数据
bpftool map dump name stats_map
#示例输出
#key: c1 c2  value: a1 a2
#Found 1 element

# 删除哈希表映射
rm /sys/fs/bpf/stats_map
```
