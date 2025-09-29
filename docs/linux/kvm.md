
# 编译 KVM
```bash
cd /usr/src/linux-4.19.90-2204.4.0.0146.oe1.x86_64
cp /boo/config-4.19.90-2204.4.0.0146.oe1.x86_64 /usr/src/linux-4.19.90-2204.4.0.0146.oe1.x86_64/.config
make olddefconfig
make -j$(nproc) -> compile.log
make modules SUBDIRS=arch/x86/kvm

# 卸载旧版本模块
modprobe -r kvm_intel && modprobe -r kvm

# 安装新版本模块
modprobe irqbypass && insmod kvm.ko && insmod kvm-intel.ko
```

# debug
## 使用 kvm_stat 查看 kvm 事件
```bash
kvm_stat -p $(pidof /usr/bin/qemu-system-x86_64)
>>
kvm statistics - pid 2137740 (openeuler-20_03)

 Event                                         Total %Total CurAvg/s
 kvm_entry                                      1133   20.5       80
 kvm_exit                                       1133   20.5       80
 kvm_hv_timer_state                             1125   20.3       80
 kvm_msr                                         816   14.7       58
 kvm_pv_tlb_flush                                293    5.3       21
 kvm_vcpu_wakeup                                 291    5.3       21
 kvm_apic_accept_irq                             287    5.2       20
 kvm_pvclock_update                              218    3.9       17
 kvm_wait_lapic_expire                           146    2.6       10
 kvm_apic                                         28    0.5        2
 kvm_apic_ipi                                     28    0.5        2
 kvm_halt_poll_ns                                 16    0.3        2
 kvm_fast_mmio                                     8    0.1        1
 kvm_msi_set_irq                                   8    0.1        1
 kvm_unmap_hva_range                               3    0.1        0
 Total                                          5533             394
```

## 使用 perf kvm stat 查看 kvm 事件
```bash
perf kvm stat live -p $(pidof /usr/bin/qemu-system-x86_64)
# 记录信息
perf kvm stat record -p $(pidof /usr/bin/qemu-system-x86_64)
perf kvm stat report
>>
Analyze events for all VMs, all VCPUs:

             VM-EXIT    Samples  Samples%     Time%    Min Time    Max Time         Avg time 

           MSR_WRITE        232    75.08%     0.00%      0.24us     15.62us      0.78us ( +-  11.73% )
                 HLT         71    22.98%   100.00%     88.90us 3315419.60us 602567.95us ( +-  14.17% )
       EPT_MISCONFIG          3     0.97%     0.00%      2.24us      3.06us      2.58us ( +-   9.65% )
  EXTERNAL_INTERRUPT          2     0.65%     0.00%      2.11us      2.38us      2.25us ( +-   6.05% )
    PREEMPTION_TIMER          1     0.32%     0.00%      1.02us      1.02us      1.02us ( +-   0.00% )

Total Samples:309, Total events handled time:42782518.51us.
```

## 通过 ftrace 查看 kvm 事件
```bash
cd /sys/kernel/debug/tracing/events/kvm
echo 1 > enable ; sleep 1 ; echo 0 > enable 
less /sys/kernel/debug/tracing/trace 
>>
# tracer: nop
#
# entries-in-buffer/entries-written: 20336/20336   #P:24
#
#                                _-----=> irqs-off
#                               / _----=> need-resched
#                              | / _---=> hardirq/softirq
#                              || / _--=> preempt-depth
#                              ||| / _-=> migrate-disable
#                              |||| /     delay
#           TASK-PID     CPU#  |||||  TIMESTAMP  FUNCTION
#              | |         |   |||||     |         |
       CPU 5/KVM-2137779 [010] d.... 798115.331413: kvm_msr: msr_write 6e0 = 0x81cba98c958c9
       CPU 5/KVM-2137779 [010] d.... 798115.331415: kvm_msr: msr_write 6e0 = 0x81cb9d4a503f2
       CPU 5/KVM-2137779 [010] d.... 798115.331416: kvm_msr: msr_write 6e0 = 0x81cb9d4806966
       CPU 5/KVM-2137779 [010] d.... 798115.331567: kvm_msr: msr_write 6e0 = 0x81cba98c958cd
       CPU 5/KVM-2137779 [010] d.... 798115.331568: kvm_msr: msr_write 6e0 = 0x81cb9d4a503f3
       CPU 5/KVM-2137779 [010] d.... 798115.331569: kvm_msr: msr_write 6e0 = 0x81cb9d488674c
       CPU 5/KVM-2137779 [010] d.... 798115.331720: kvm_msr: msr_write 6e0 = 0x81cba98c958c1
       CPU 5/KVM-2137779 [010] d.... 798115.331721: kvm_msr: msr_write 6e0 = 0x81cb9d4a503e4
       CPU 5/KVM-2137779 [010] d.... 798115.331722: kvm_msr: msr_write 6e0 = 0x81cb9d490617a

# 查看 msr 事件
cd /sys/kernel/debug/tracing/events/kvm/kvm_msr/ 
echo 1 > enable ; sleep 1 ; echo 0 > enable 
less /sys/kernel/debug/tracing/trace
>>
# tracer: nop
#
# entries-in-buffer/entries-written: 20432/20432   #P:24
#
#                                _-----=> irqs-off
#                               / _----=> need-resched
#                              | / _---=> hardirq/softirq
#                              || / _--=> preempt-depth
#                              ||| / _-=> migrate-disable
#                              |||| /     delay
#           TASK-PID     CPU#  |||||  TIMESTAMP  FUNCTION
#              | |         |   |||||     |         |
       CPU 5/KVM-2137779 [010] d.... 798115.331413: kvm_msr: msr_write 6e0 = 0x81cba98c958c9
       CPU 5/KVM-2137779 [010] d.... 798115.331415: kvm_msr: msr_write 6e0 = 0x81cb9d4a503f2
       CPU 5/KVM-2137779 [010] d.... 798115.331416: kvm_msr: msr_write 6e0 = 0x81cb9d4806966
       CPU 5/KVM-2137779 [010] d.... 798115.331567: kvm_msr: msr_write 6e0 = 0x81cba98c958cd
       CPU 5/KVM-2137779 [010] d.... 798115.331568: kvm_msr: msr_write 6e0 = 0x81cb9d4a503f3
       CPU 5/KVM-2137779 [010] d.... 798115.331569: kvm_msr: msr_write 6e0 = 0x81cb9d488674c
       CPU 5/KVM-2137779 [010] d.... 798115.331720: kvm_msr: msr_write 6e0 = 0x81cba98c958c1
       CPU 5/KVM-2137779 [010] d.... 798115.331721: kvm_msr: msr_write 6e0 = 0x81cb9d4a503e4
```

## 查看虚拟机热点调用
```bash
# 登录虚拟机或内核相同的虚拟机，导出符号表和内核模块
cat /proc/kallsyms > /tmp/guest.kallsyms
cat /proc/modules > /tmp/guest.modules



```
[perf kvm查看虚机热点调用](https://blog.csdn.net/lonely_geek/article/details/121298201)

## 查看热点调用
```bash
perf record -p $(pidof /usr/bin/qemu-system-x86_64)
perf report
```

# 其他
```bash
systemctl stop kdump && systemctl disable kdump
echo c > /proc/sysrq-trigger
```

[kvm 虚拟机qcow2磁盘格式扩容](https://cpp.la/514.html)
