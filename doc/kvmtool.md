# 安装使用
## 编译 kvmtool
```sh
git clone git://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git
cd kvmtool
make -j$(nproc)
# 将生成的 kvmtool 可执行文件拷贝到 /usr/local/bin
sudo cp lkvm /usr/local/bin
```

## 编译 linux
```sh
wget https://mirrors.tuna.tsinghua.edu.cn/kernel/v4.x/linux-4.19.tar.gz
tar -xvf linux-4.19.tar.gz
cd linux-4.19
# 配置需默认包含的模块
make menuconfig
# 需要开启以下选项
>>
 - For the default console output:
	CONFIG_SERIAL_8250=y
	CONFIG_SERIAL_8250_CONSOLE=y

-> Device Drivers                                                   
  -> Character devices                                              
    -> Serial drivers                                               
     -> 8250/16550 and compatible serial support (SERIAL_8250 [=y])


 - For running 32bit images on 64bit hosts:
	CONFIG_IA32_EMULATION=y

 - Proper FS options according to image FS (e.g. CONFIG_EXT2_FS, CONFIG_EXT4_FS).

 - For all virtio devices listed below:
	CONFIG_VIRTIO=y
	CONFIG_VIRTIO_RING=y
	CONFIG_VIRTIO_PCI=y

-> Device Drivers                     
  -> Virtio drivers (VIRTIO_MENU [=y])


 - For virtio-blk devices (--disk, -d):
	CONFIG_VIRTIO_BLK=y

-> Device Drivers                
  -> Block devices (BLK_DEV [=y])


 - For virtio-net devices ([--network, -n] virtio):
	CONFIG_VIRTIO_NET=y

-> Device Drivers                                 
  -> Network device support (NETDEVICES [=y])     
    -> Network core driver support (NET_CORE [=y])
    -> Virtio network driver


 - For virtio-9p devices (--virtio-9p):
	CONFIG_NET_9P=y
	CONFIG_NET_9P_VIRTIO=y
	CONFIG_9P_FS=y

-> Networking support (NET [=y])                            
  -> Plan 9 Resource Sharing Support (9P2000) (NET_9P [=y]) 
     -> File systems                                      
         -> Network File Systems (NETWORK_FILESYSTEMS [=y]) 


 - For virtio-balloon device (--balloon):
	CONFIG_VIRTIO_BALLOON=y

-> Device Drivers                      
  -> Virtio drivers (VIRTIO_MENU [=y]) 


 - For virtio-console device (--console virtio):
	CONFIG_VIRTIO_CONSOLE=y

-> Device Drivers     
  -> Character devices


 - For virtio-rng device (--rng):
	CONFIG_HW_RANDOM_VIRTIO=y

-> Device Drivers                                                    
  -> Character devices                                               
    -> Hardware Random Number Generator Core support (HW_RANDOM [=y])


 - For vesa device (--sdl or --vnc):
	CONFIG_FB_VESA=y

-> Device Drivers                                  
  -> Graphics support                              
    -> Frame buffer Devices                        
      -> Support for frame buffer devices (FB [=y])

# 需默认开启的模块
# https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/about/

# 编译
make -j$(nproc)
```
编译完成之后在 /arch/x86/boot/ 目录下生成 bzImage 文件。


## 制作根文件系统
busybox 是一个集成了多个最常用 linux 命令和工具的软件，可以用来制作根文件系统。
```sh
wget https://busybox.net/downloads/busybox-1.35.0.tar.bz2
tar -xvf busybox-1.35.0.tar.bz2
cd busybox-1.35.0/
make menuconfig
# 配置为静态编译
-> Settings
  -> Build Options
    -> Build BusyBox as a static binary (no shared libs)

# 编译并安装
make -j$(nproc)
make install
```
完成之后会在编译目录下生成 _install 目录（`bin/linuxrc/sbin/usr`），主要包含一些可执行文件，此后需要将这些文件方的放到 rootfs。

制作 rootfs
```sh
# 创建镜像
dd if=/dev/zero of=rootfs.img bs=1M count=1024
# 格式化为 ext4 文件系统
mkfs.ext4 -m 0 -O none -F rootfs.img
# 挂载镜像
mkdir rootfs
sudo mount -o loop rootfs.img rootfs

# 在 rootfs 中创建 linux 的根目录树：
sudo cp busybox-1.35.0/_install/* rootfs/ -raf
# rootfs 目录中新建 linux 根目录树
cd busybox-1.35.0/
sudo mkdir  dev  etc  lib  var  proc  tmp  home  root  mnt  sys

ls
>> bin  dev  etc  home  lib  linuxrc  lost+found  mnt  proc  root  sbin  sys  tmp  usr  var
# 各目录说明如下:
# /dev: 存储特殊文件或设备文件
# /etc: 系统配置文件
# /home: 普通用户目录
# /lib: 为系统启动或根文件上的应用程序（/bin,/sbin等）提供共享库，以及为内核提供内核模块
# /bin: 系统管理员和用户均可使用的命令
# /sbin： 系统管理员使用的系统命令
# /root：root用户目录
# /mnt：临时挂载点
# /proc: 基于内存的虚拟文件系统，用于为内核及进程存储其相关信息
# /sys：sysfs虚拟文件系统提供了一种比proc更为理想的访问内核数据的途径：其主要作用在于为管理linux设备提供一种统一模型的接口；
# /usr：usr hierarchy，全局共享的只读数据路径
# /var：存储常发生变化的数据目录：cache、log等
# /tmp: 临时文件存储目录

# 拷贝 busybox 的配置目录，包含：fstab/init.d/inittab/profile
cd ..
sudo cp busybox-1.35.0/examples/bootfloppy/etc/*  rootfs/etc -r
```

创建根目录所必需的文件
```sh
# 修改 fstab
cd rootfs/
cat> etc/fstab << EOF
proc  /proc proc  defaults 0 0
tmpfs  /tmp  tmpfs  defaults 0 0
none  /tmp  ramfs defaults 0 0
sysfs /sys  sysfs defaults 0 0
mdev  /dev  ramfs defaults 0 0
EOF

# 修改 profile
cd rootfs/
cat> etc/fstab << EOF
# /etc/profile: system-wide .profile file for the Bourne shells

PATH=/bin:/sbin:/usr/bin:/usr/sbin #可执行程序 环境变量
export LD_LIBRARY_PATH=/lib:/usr/lib #动态链接库 环境变量
/bin/hostname kvmtool-test
USER="`id -un`"
LOGNAME=$USER
HOSTNAME='/bin/hostname'
PS1='[\u@\h \W]# ' #显示主机名、当前路径等信息
EOF

# 修改 initab
cd rootfs/
cat > etc/inittab << EOF
::sysinit:/etc/init.d/rcS
tty0::askfirst:-/bin/sh
::respawn:-/bin/sh
::askfirst:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
EOF
chmod 755 etc/inittab

# 修改 rcS
cd rootfs/
cat > etc/init.d/rcS << EOF
/bin/mount -a
mkdir -p /dev/pts
mount -t devpts devpts /dev/pts
echo /sbin/mdev > /proc/sys/kernel/hotplug
mdev -s
echo "************Welcome to mini Linux************"
EOF
chmod 755 etc/init.d/rcS

# 添加设备文件
cd dev
mknod console c 5 1
mknod null c 1 3
mknod tty1 c 4 1
cd -
```

## 启动虚拟机
```sh
lkvm run --kernel linux-4.19.288/arch/x86/boot/bzImage --disk rootfs.img --network virtio --console serial  --name vm1
>>
  Info: # lkvm run -k linux-4.19.288/arch/x86/boot/bzImage -m 448 -c 4 --name vm1
[    0.000000] Linux version 4.19.288 (jipeng@rvm) (gcc version 11.3.0 (Ubuntu 11.3.0-1ubuntu1~22.04.1)) #1 SMP Sun Jul 23 09:56:54 CST 2023
[    0.000000] Command line: noapic noacpi pci=conf1 reboot=k panic=1 i8042.direct=1 i8042.dumbkbd=1 i8042.nopnp=1 earlyprintk=serial i8042.noaux=1 console=ttyS0 root=/dev/vda rw 
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
[    0.000000]   Centaur CentaurHauls
[    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[    0.000000] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[    0.000000] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[    0.000000] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'standard' format.
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000ffffe] reserved
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x000000001bffffff] usable
[    0.000000] bootconsole [earlyser0] enabled
[    0.000000] ERROR: earlyprintk= earlyser already used
[    0.000000] NX (Execute Disable) protection: active
[    0.000000] DMI not present or invalid.
[    0.000000] Hypervisor detected: KVM
[    0.000000] kvm-clock: Using msrs 4b564d01 and 4b564d00
[    0.000001] kvm-clock: cpu 0, msr 15a01001, primary cpu clock
[    0.000001] kvm-clock: using sched offset of 188064562 cycles
[    0.000893] clocksource: kvm-clock: mask: 0xffffffffffffffff max_cycles: 0x1cd42e4dffb, max_idle_ns: 881590591483 ns
[    0.003488] tsc: Detected 2893.426 MHz processor
[    0.004535] last_pfn = 0x1c000 max_arch_pfn = 0x400000000
[    0.005518] Disabled
[    0.005868] x86/PAT: MTRRs disabled, skipping PAT initialization too.
[    0.006930] CPU MTRRs all blank - virtualized system.
[    0.007762] x86/PAT: Configuration [0-7]: WB  WT  UC- UC  WB  WT  UC- UC  
Memory KASLR using RDRAND RDTSC...
[    0.010003] found SMP MP-table at [mem 0x000f0370-0x000f037f]
[    0.011405] Scanning 1 areas for low memory corruption
[    0.014245] ACPI: Early table checksum verification disabled
[    0.015453] ACPI BIOS Error (bug): A valid RSDP was not found (20180810/tbxfroot-210)
[    0.017287] No NUMA configuration found
[    0.017920] Faking a node at [mem 0x0000000000000000-0x000000001bffffff]
[    0.019021] NODE_DATA(0) allocated [mem 0x1bfd6000-0x1bffffff]
[    0.020411] Zone ranges:
[    0.020830]   DMA      [mem 0x0000000000001000-0x0000000000ffffff]
[    0.021883]   DMA32    [mem 0x0000000001000000-0x000000001bffffff]
[    0.022865]   Normal   empty
[    0.023322]   Device   empty
[    0.023782] Movable zone start for each node
[    0.024380] Early memory node ranges
[    0.024719]   node   0: [mem 0x0000000000001000-0x000000000009efff]
[    0.025535]   node   0: [mem 0x0000000000100000-0x000000001bffffff]
[    0.027483] Zeroed struct page in unavailable ranges: 16482 pages
[    0.027486] Initmem setup node 0 [mem 0x0000000000001000-0x000000001bffffff]
[    0.038070] Intel MultiProcessor Specification v1.4
[    0.038886] MPTABLE: OEM ID: KVMCPU00
[    0.039471] MPTABLE: Product ID: 0.1         
[    0.040127] MPTABLE: APIC at: 0xFEE00000
[    0.040893] Processor #0 (Bootup-CPU)
[    0.041560] Processor #1
[    0.041977] Processor #2
[    0.042394] Processor #3
[    0.042882] IOAPIC[0]: apic_id 5, version 17, address 0xfec00000, GSI 0-23
[    0.044017] Processors: 4
[    0.044461] smpboot: Allowing 4 CPUs, 0 hotplug CPUs
[    0.045354] PM: Registered nosave memory: [mem 0x00000000-0x00000fff]
[    0.046403] PM: Registered nosave memory: [mem 0x0009f000-0x0009ffff]
[    0.047444] PM: Registered nosave memory: [mem 0x000a0000-0x000effff]
[    0.048491] PM: Registered nosave memory: [mem 0x000f0000-0x000fefff]
[    0.049510] PM: Registered nosave memory: [mem 0x000ff000-0x000fffff]
[    0.050575] [mem 0x1c000000-0xffffffff] available for PCI devices
[    0.051565] Booting paravirtualized kernel on KVM
[    0.052339] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645519600211568 ns
[    0.054057] setup_percpu: NR_CPUS:8192 nr_cpumask_bits:4 nr_cpu_ids:4 nr_node_ids:1
[    0.056921] percpu: Embedded 51 pages/cpu s172032 r8192 d28672 u524288
[    0.058065] KVM setup async PF for cpu 0
[    0.058709] kvm-stealtime: cpu 0, msr 1b229040
[    0.059458] PV qspinlock hash table entries: 256 (order: 0, 4096 bytes)
[    0.060544] Built 1 zonelists, mobility grouping on.  Total pages: 112777
[    0.061642] Policy zone: DMA32
[    0.062145] Kernel command line: noapic noacpi pci=conf1 reboot=k panic=1 i8042.direct=1 i8042.dumbkbd=1 i8042.nopnp=1 earlyprintk=serial i8042.noaux=1 console=ttyS0 root=/dev/vda rw 
[    0.066433] Memory: 401704K/458360K available (14348K kernel code, 3895K rwdata, 4300K rodata, 2628K init, 17924K bss, 56656K reserved, 0K cma-reserved)
[    0.069013] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=4, Nodes=1
[    0.070142] Kernel/User page tables isolation: enabled
[    0.071013] ftrace: allocating 41047 entries in 161 pages
[    0.089481] rcu: Hierarchical RCU implementation.
[    0.090217] rcu: 	RCU restricting CPUs from NR_CPUS=8192 to nr_cpu_ids=4.
[    0.091299] rcu: Adjusting geometry for rcu_fanout_leaf=16, nr_cpu_ids=4
[    0.094597] NR_IRQS: 524544, nr_irqs: 456, preallocated irqs: 16
[    0.095759] random: crng init done
[    0.096390] Console: colour *CGA 80x25
[    0.097084] console [ttyS0] enabled
[    0.097084] console [ttyS0] enabled
[    0.098220] bootconsole [earlyser0] disabled
[    0.098220] bootconsole [earlyser0] disabled
[    0.099768] APIC: Switch to symmetric I/O mode setup
[    0.100655] Not enabling interrupt remapping due to skipped IO-APIC setup
[    0.102056] KVM setup pv IPIs
[    0.102772] clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x29b500ca33a, max_idle_ns: 440795203665 ns
[    0.104835] Calibrating delay loop (skipped) preset value.. 5786.85 BogoMIPS (lpj=11573704)
[    0.106284] pid_max: default: 32768 minimum: 301
[    0.107108] Security Framework initialized
[    0.108818] Yama: becoming mindful.
[    0.109454] AppArmor: AppArmor initialized
[    0.110657] Dentry cache hash table entries: 65536 (order: 7, 524288 bytes)
[    0.112087] Inode-cache hash table entries: 32768 (order: 6, 262144 bytes)
[    0.112836] Mount-cache hash table entries: 1024 (order: 1, 8192 bytes)
[    0.113969] Mountpoint-cache hash table entries: 1024 (order: 1, 8192 bytes)
[    0.115575] x86/cpu: Activated the Intel User Mode Instruction Prevention (UMIP) CPU feature
[    0.116994] Last level iTLB entries: 4KB 512, 2MB 8, 4MB 8
[    0.117987] Last level dTLB entries: 4KB 512, 2MB 32, 4MB 32, 1GB 0
[    0.119063] Spectre V1 : Mitigation: usercopy/swapgs barriers and __user pointer sanitization
[    0.120816] Spectre V2 : Mitigation: Retpolines
[    0.121607] Spectre V2 : Spectre v2 / SpectreRSB mitigation: Filling RSB on context switch
[    0.122977] Spectre V2 : Spectre v2 / SpectreRSB : Filling RSB on VMEXIT
[    0.124810] Speculative Store Bypass: Vulnerable
[    0.125669] MDS: Vulnerable: Clear CPU buffers attempted, no microcode
[    0.126760] MMIO Stale Data: Unknown: No mitigations
[    0.127574] SRBDS: Unknown: Dependent on hypervisor status
[    0.129239] Freeing SMP alternatives memory: 36K
[    0.352196] smpboot: CPU0: Intel 06/3a (family: 0x6, model: 0x3a, stepping: 0x8)
[    0.352805] Performance Events: IvyBridge events, full-width counters, Intel PMU driver.
[    0.352805] ... version:                2
[    0.352805] ... bit width:              48
[    0.352809] ... generic registers:      4
[    0.353497] ... value mask:             0000ffffffffffff
[    0.354346] ... max period:             00007fffffffffff
[    0.355231] ... fixed-purpose events:   3
[    0.355916] ... event mask:             000000070000000f
[    0.356968] rcu: Hierarchical SRCU implementation.
[    0.359162] smp: Bringing up secondary CPUs ...
[    0.361128] x86: Booting SMP configuration:
[    0.362510] .... node  #0, CPUs:      #1
[    0.009056] kvm-clock: cpu 1, msr 15a01041, secondary cpu clock
[    0.009056] x86/cpu: Activated the Intel User Mode Instruction Prevention (UMIP) CPU feature
[    0.009056] [Firmware Bug]: CPU1: APIC id mismatch. Firmware: 1 APIC: 0
[    0.367746] KVM setup async PF for cpu 1
[    0.367746] kvm-stealtime: cpu 1, msr 1b2a9040
[    0.369166]  #2
[    0.009056] kvm-clock: cpu 2, msr 15a01081, secondary cpu clock
[    0.009056] x86/cpu: Activated the Intel User Mode Instruction Prevention (UMIP) CPU feature
[    0.374198] KVM setup async PF for cpu 2
[    0.374198] kvm-stealtime: cpu 2, msr 1b329040
[    0.376838] MDS CPU bug present and SMT on, data leak possible. See https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/mds.html for more details.
[    0.379727]  #3
[    0.009056] kvm-clock: cpu 3, msr 15a010c1, secondary cpu clock
[    0.009056] x86/cpu: Activated the Intel User Mode Instruction Prevention (UMIP) CPU feature
[    0.009056] [Firmware Bug]: CPU3: APIC id mismatch. Firmware: 3 APIC: 0
[    0.384846] KVM setup async PF for cpu 3
[    0.385509] kvm-stealtime: cpu 3, msr 1b3a9040
[    0.386319] smp: Brought up 1 node, 4 CPUs
[    0.386319] smpboot: Max logical packages: 1
[    0.386319] smpboot: Total of 4 processors activated (23147.40 BogoMIPS)
[    0.389686] devtmpfs: initialized
[    0.389686] x86/mm: Memory block size: 128MB
[    0.390549] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 7645041785100000 ns
[    0.392847] futex hash table entries: 1024 (order: 4, 65536 bytes)
[    0.394125] pinctrl core: initialized pinctrl subsystem
[    0.395381] RTC time:  8:26:26, date: 07/23/23
[    0.397134] NET: Registered protocol family 16
[    0.397948] audit: initializing netlink subsys (disabled)
[    0.398898] audit: type=2000 audit(1690100786.475:1): state=initialized audit_enabled=0 res=1
[    0.400816] cpuidle: using governor ladder
[    0.401529] cpuidle: using governor menu
[    0.401638] KVM setup pv remote TLB flush
[    0.402490] PCI: Using configuration type 1 for base access
[    0.403519] core: PMU erratum BJ122, BV98, HSD29 worked around, HT is on
[    0.406265] HugeTLB registered 2.00 MiB page size, pre-allocated 0 pages
[    0.408969] ACPI: Interpreter disabled.
[    0.408969] vgaarb: loaded
[    0.409620] SCSI subsystem initialized
[    0.412971] usbcore: registered new interface driver usbfs
[    0.412971] usbcore: registered new interface driver hub
[    0.413841] usbcore: registered new device driver usb
[    0.414734] pps_core: LinuxPPS API ver. 1 registered
[    0.415572] pps_core: Software ver. 5.3.6 - Copyright 2005-2007 Rodolfo Giometti <giometti@linux.it>
[    0.416815] PTP clock support registered
[    0.417503] EDAC MC: Ver: 3.0.0
[    0.417503] PCI: Probing PCI hardware
[    0.417593] PCI host bridge to bus 0000:00
[    0.418274] pci_bus 0000:00: root bus resource [io  0x0000-0xffff]
[    0.420811] pci_bus 0000:00: root bus resource [mem 0x00000000-0xfffffffff]
[    0.422047] pci_bus 0000:00: No busn resource found for root bus, will use [bus 00-ff]
[    0.432359] NetLabel: Initializing
[    0.432809] NetLabel:  domain hash size = 128
[    0.433548] NetLabel:  protocols = UNLABELED CIPSOv4 CALIPSO
[    0.434511] NetLabel:  unlabeled traffic allowed by default
[    0.436950] clocksource: Switched to clocksource kvm-clock
[    0.459396] VFS: Disk quotas dquot_6.6.0
[    0.460118] VFS: Dquot-cache hash table entries: 512 (order 0, 4096 bytes)
[    0.461565] AppArmor: AppArmor Filesystem Enabled
[    0.462406] pnp: PnP ACPI: disabled
[    0.466895] NET: Registered protocol family 2
[    0.467752] IP idents hash table entries: 8192 (order: 4, 65536 bytes)
[    0.469334] tcp_listen_portaddr_hash hash table entries: 256 (order: 0, 4096 bytes)
[    0.470777] TCP established hash table entries: 4096 (order: 3, 32768 bytes)
[    0.472004] TCP bind hash table entries: 4096 (order: 4, 65536 bytes)
[    0.474163] TCP: Hash tables configured (established 4096 bind 4096)
[    0.475431] UDP hash table entries: 256 (order: 1, 8192 bytes)
[    0.476419] UDP-Lite hash table entries: 256 (order: 1, 8192 bytes)
[    0.477518] NET: Registered protocol family 1
[    0.478265] NET: Registered protocol family 44
[    0.479218] clocksource: tsc: mask: 0xffffffffffffffff max_cycles: 0x29b500ca33a, max_idle_ns: 440795203665 ns
[    0.480904] platform rtc_cmos: registered platform RTC device (no PNP device found)
[    0.482204] Scanning for low memory corruption every 60 seconds
[    0.484067] Initialise system trusted keyrings
[    0.484872] Key type blacklist registered
[    0.485672] workingset: timestamp_bits=36 max_order=17 bucket_order=0
[    0.488207] zbud: loaded
[    0.489236] squashfs: version 4.0 (2009/01/31) Phillip Lougher
[    0.490708] fuse init (API version 7.27)
[    0.491501] 9p: Installing v9fs 9p2000 file system support
[    0.496693] Key type asymmetric registered
[    0.497525] Asymmetric key parser 'x509' registered
[    0.498362] Block layer SCSI generic (bsg) driver version 0.4 loaded (major 243)
[    0.499741] io scheduler noop registered
[    0.500379] io scheduler deadline registered
[    0.502666] io scheduler cfq registered (default)
[    0.503467] io scheduler mq-deadline registered
[    0.504603] shpchp: Standard Hot Plug PCI Controller Driver version: 0.4
[    0.507643] Serial: 8250/16550 driver, 32 ports, IRQ sharing enabled
[    0.530348] serial8250: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a U6_16550A
[    0.553734] serial8250: ttyS1 at I/O 0x2f8 (irq = 3, base_baud = 115200) is a U6_16550A
[    0.576628] serial8250: ttyS2 at I/O 0x3e8 (irq = 4, base_baud = 115200) is a U6_16550A
[    0.579828] Linux agpgart interface v0.103
[    0.584201] loop: module loaded
[    0.590033] virtio_blk virtio1: [vda] 2097152 512-byte logical blocks (1.07 GB/1.00 GiB)
[    0.592316] tun: Universal TUN/TAP device driver, 1.6
[    0.597082] PPP generic driver version 2.4.2
[    0.597954] VFIO - User Level meta-driver version: 0.3
[    0.599205] ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
[    0.600336] ehci-pci: EHCI PCI platform driver
[    0.601218] ehci-platform: EHCI generic platform driver
[    0.602013] ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
[    0.603048] ohci-pci: OHCI PCI platform driver
[    0.603803] ohci-platform: OHCI generic platform driver
[    0.604653] uhci_hcd: USB Universal Host Controller Interface driver
[    0.605372] i8042: PNP detection disabled
[    0.605987] serio: i8042 KBD port at 0x60,0x64 irq 1
[    0.606996] mousedev: PS/2 mouse device common for all mice
[    0.607945] input: AT Raw Set 2 keyboard as /devices/platform/i8042/serio0/input/input0
[    0.609054] rtc_cmos rtc_cmos: only 24-hr supported
[    0.610449] i2c /dev entries driver
[    0.611166] device-mapper: uevent: version 1.0.3
[    0.612079] device-mapper: ioctl: 4.39.0-ioctl (2018-04-03) initialised: dm-devel@redhat.com
[    0.613853] ledtrig-cpu: registered to indicate activity on CPUs
[    0.614999] drop_monitor: Initializing network drop monitor service
[    0.616231] NET: Registered protocol family 10
[    0.618270] Segment Routing with IPv6
[    0.618929] NET: Registered protocol family 17
[    0.619772] 9pnet: Installing 9P2000 support
[    0.620503] Key type dns_resolver registered
[    0.621862] mce: Using 32 MCE banks
[    0.622474] RAS: Correctable Errors collector initialized.
[    0.623434] sched_clock: Marking stable (616756117, 5056322)->(624699105, -2886666)
[    0.627117] registered taskstats version 1
[    0.627981] Loading compiled-in X.509 certificates
[    0.629739] Loaded X.509 cert 'Build time autogenerated kernel key: 3d8da49ac4e712fa10d5ccb2f5dc608ebbdd24c2'
[    0.631470] zswap: loaded using pool lzo/zbud
[    0.632412] Key type trusted registered
[    0.633470] Key type encrypted registered
[    0.634155] AppArmor: AppArmor sha1 policy hashing enabled
[    0.635070] ima: No TPM chip found, activating TPM-bypass!
[    0.635970] ima: Allocated hash algorithm: sha1
[    0.636677] evm: Initialising EVM extended attributes:
[    0.637557] evm: security.selinux
[    0.638104] evm: security.SMACK64
[    0.638595] evm: security.SMACK64EXEC
[    0.638944] evm: security.SMACK64TRANSMUTE
[    0.639327] evm: security.SMACK64MMAP
[    0.639708] evm: security.apparmor
[    0.640274] evm: security.ima
[    0.640767] evm: security.capability
[    0.641411] evm: HMAC attrs: 0x1
[    0.642378]   Magic number: 15:954:422
[    0.643075] hctosys: unable to open rtc device (rtc0)
[    0.644290] md: Waiting for all devices to be available before autodetect
[    0.645454] md: If you don't use raid, use raid=noautodetect
[    0.646655] md: Autodetecting RAID arrays.
[    0.647488] md: autorun ...
[    0.647966] md: ... autorun DONE.
[    0.648934] EXT4-fs (vda): mounting ext2 file system using the ext4 subsystem
[    0.651160] EXT4-fs (vda): warning: mounting unchecked fs, running e2fsck is recommended
[    0.688082] EXT4-fs (vda): mounted filesystem without journal. Opts: (null)
[    0.689311] VFS: Mounted root (ext2 filesystem) on device 253:0.
[    0.691267] devtmpfs: mounted
[    0.694265] Freeing unused decrypted memory: 2040K
[    0.696144] Freeing unused kernel image memory: 2628K
[    0.705028] Write protecting the kernel read-only data: 22528k
[    0.707489] Freeing unused kernel image memory: 2008K
[    0.709583] Freeing unused kernel image memory: 1844K
[    0.722041] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    0.723211] x86/mm: Checking user space page tables
[    0.735349] x86/mm: Checked W+X mappings: passed, no W+X pages found.
[    0.736470] Run /sbin/init as init process
************Welcome to mini Linux************

```

## 进入 guest OS 配置网络
```sh
ip link list
ip link set eth0 up
ip addr add 192.168.33.100/24 dev eth0
ip a
```


[kvmtool](https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/about/)  
[kvmtool - a QEMU alternative?](https://elinux.org/images/4/44/Przywara.pdf)  
