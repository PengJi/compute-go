介绍与使用虚拟化技术

## CPU 虚拟化
x86 架构下的 VMX 扩展  
VMX 下 vCPU 的完整生命周期  
Host 与 Guest 的切换  
指令的模拟  
KVM 虚拟多处理器  

## 内存虚拟化
操作系统如何为虚拟机呈现物理内存  
KVM 利用影子页表和 EPT 实现从 GVA 到 HPA 的 2 层地址映射  

## 中断虚拟化
8259A 的中断  
多核系统的 APIC   
I/O APIC  
从设备直接向 LAPIC 发送 MSI  
Intel 硬件层面支持虚拟化中断  

## 外设虚拟化
设备虚拟化的基本原理  
半虚拟化（virtio）  
Intel VT-d 硬件辅助虚拟化  
支持 SR-IOV 的 DMA 重映射  
中断重映射  

## 网络虚拟化
操作系统虚拟专用网络设备  

## tags
**MMU**  **IOMMU**  **DMA(Direct Memory Access)**  **中断重映射(Interrupt Remapping)**  **virtio**  **vhost**  **vhost-user** 


# Type-1 hypervisor
Type-1 hypervisor 是一种直接运行在物理硬件上的虚拟化解决方案，其直接管理硬件资源并将其分配给各个虚拟机。

## KVM
KVM 是 Linux 内核的一个模块，可以使 Linux 成为一个 type-1 hypervisor。KVM 支持多种客户端操作系统，包括 Windows、Linux 和 macOS。KVM 通常与其他管理工具（如 libvirt 和 QEMU）结合使用，以提供完整的虚拟化解决方案。
* 基于内核：KVM 作为 Linux 内核的一部分，可以充分利用内核的功能和性能优势，如调度、内存管理等。
* 高性能：KVM 通过使用虚拟化扩展（VT）来提供硬件虚拟化功能，这些扩展由 Intel 和 AMD 提供。KVM 通过使用 Intel VT-x 或 AMD-V 来提供硬件虚拟化功能。这使得 KVM 能够实现接近原生性能的运行速度。
* 跨平台支持：KVM 支持多种客户操作系统，如 Windows、Linux、BSD 等。此外，KVM 还支持多种处理器架构，如 x86、ARM、PowerPC 等。
* 与 QEMU 集成：KVM 通常与 QEMU 一起使用，KVM 提供 CPU、内存、中断相关的虚拟机，QEMU 负责提供设备模拟和其他辅助功能。KVM 和 QEMU 的结合使得虚拟机管理和资源分配更加灵活。
* 丰富的功能：ESXi 提供了许多企业级功能，如虚拟机快照、动态资源调度、高可用性（HA）、分布式资源调度（DRS）和虚拟 SAN 等。
* 管理工具：ESXi 可以与 VMware vCenter Server 集成，提供集中管理的虚拟化环境。通过 vSphere Client 或 vSphere Web Client，管理员可以轻松地执行各种虚拟机管理任务。
* 安全性：ESXi 具有内置的安全功能，如安全引导、虚拟 TPM、加密的虚拟机等，以确保虚拟化环境的安全性。
* 跨平台支持：ESXi 支持多种客户操作系统，如 Windows、Linux、BSD 等。这使得 ESXi 可以适应各种业务需求。


## VMware ESXi
VMware ESXi 是一种由 VMware 公司开发和维护的 Type-1 Hypervisor。ESXi 是 VMware vSphere 虚拟化平台的核心组件，专为企业级虚拟化环境设计。ESXi 可以运行在物理服务器上，将其硬件资源分割为多个虚拟机（VM），从而实现多个操作系统并行运行。
ESXi 与 VMware vCenter Server 配合使用，可以实现虚拟机的集中管理、监控、备份、迁移等功能。ESXi 与 vCenter Server 之间的通信通过 VMware vSphere API 实现。
* 高性能：ESXi 利用硬件虚拟化技术（如 Intel VT-x 和 AMD-V）实现高性能的虚拟化解决方案。ESXi 能够实现接近原生性能的运行速度，支持大规模的虚拟机部署。


## Microsoft Hyper-V
Microsoft Hyper-V 是Microsoft 开发和维护 Type-1 Hypervisor。Hyper-V 首次出现在 Windows Server 2008，并作为 Microsoft 服务器操作系统的核心虚拟化组件，为企业级虚拟化环境提供支持。从 Windows 8 开始，Microsoft 也开始为客户端操作系统提供 Hyper-V 版本，允许用户在其个人电脑上运行虚拟机。
* 高性能：Hyper-V 利用硬件虚拟化技术（如 Intel VT-x 和 AMD-V）实现高性能的虚拟化解决方案。Hyper-V 能够为大型虚拟机提供良好的性能和稳定性。
* 丰富的功能：Hyper-V 提供了许多企业级功能，如虚拟机快照、动态内存、网络虚拟化、虚拟硬盘和虚拟机复制等。
* 管理工具：Hyper-V 可以与 Microsoft System Center Virtual Machine Manager (SCVMM) 集成，提供集中管理的虚拟化环境。通过 Hyper-V Manager 或 PowerShell，管理员可以轻松地执行各种虚拟机管理任务。
* 安全性：Hyper-V 具有内置的安全功能，如安全启动、虚拟 TPM、虚拟机隔离等，以确保虚拟化环境的安全性。
* 跨平台支持：Hyper-V 支持多种客户操作系统，如 Windows、Linux、FreeBSD 等。这使得 Hyper-V 可以适应各种业务需求。


## Xen
Xen 是一种开源的虚拟化技术，它是一个高性能、安全且可扩展的 Type-1 Hypervisor，最早由剑桥大学的计算机实验室开发。自 2003 年首次发布以来，Xen 已经成为许多大型云基础设施（如 Amazon Web Services、Rackspace Cloud 等）的核心组成部分。


## [Xvisor](https://github.com/xvisor/xvisor)
Xvisor 是一个开源的 Type-1 虚拟机监视器（hypervisor），旨在提供一个统一的、轻量级、可移植和灵活的虚拟化解决方案，支持 ARMv7a-ve、ARMv8a、x86_64、RISC-V 等架构。
Xvisor 主要支持完全虚拟化，因此支持广泛的未经修改的客户操作系统，它同时也支持半虚拟机化（可选），并且将以与体系结构无关的方式（例如 VirtIO PCI/MMIO 设备）进行支持，以确保在使用半虚拟化时客户操作系统无需更改。
它具有现代 hypersivor 所具有的大部分特性：
* 基于配置的设备数；
* 线程框架；
* 主机设备驱动框架；
* IO 设备模拟框架；
* 运行时可加载模块；
* 直通硬件访问；
* 动态创建、销毁客户机；
* 管理终端；
* 网络虚拟化；
* 输入设备虚拟化；
* 显示设备虚拟化；
* 以及更多功能；


## [Bao](https://github.com/bao-project/bao-hypervisor)
Bao（来中国普通话“保护”的意思）是一个轻量级的开源嵌入式虚拟机监视器，旨在提供强大的隔离和实时保障。Bao 提供了一个最小化的、从零开始的分区式虚拟机监视器架构实现，支持 ARMv8-A 和 RISC-V。
* Bao 主要针对混合关键性系统，强烈关注故障隔离和实时行为。
* 实现只包括一个最小化的特权软件，利用 ISA 虚拟化支持来实现静态分区虚拟机监视器架构：资源在虚拟机实例化时静态分区并分配；内存使用两级转换静态分配；IO 仅通过直通；虚拟中断直接映射到物理中断；并实现虚拟 CPU 到物理 CPU 的 1-1 映射，无需调度器。
* Bao 没有外部依赖，例如运行不可信的、庞大的单体通用操作系统（如 Linux）的特权虚拟机，因此具有更小的可信计算基础（TCB）


## [RVirt](https://github.com/mit-pdos/RVirt)
RVirt 是一个基于 RISC-V 的 S-mode 陷入仿真的 hypervisor。它目前针对的是 QEMU 的 virt machine type，但也部分支持 HiFive Unleashed。它可以在Berkeley Boot Loader 上运行，也可以使用它自己的（明显更快的）M-mode stub。它功能强大，可以运行多个 Linux 实例作为客户操作系统。RVirt 不需要 KVM 或 Linux，可以在任何具有 MMU 的足够强大的 64 位 RISC-V 处理器上运行。


# Type-2 hypervisor
Type-2 hypervisor 是一种在宿主机操作系统（如 Linux、Windows 或 macOS）上运行的虚拟化软件。它们通常以用户模式运行，因此它们的性能不如 Type-1 hypervisor。但是，由于它们不需要修改宿主机操作系统，因此它们可以在任何操作系统上运行。包括：
* `VMware Workstation`：VMware Workstation 是一款流行的 type-2 hypervisor，可在 Windows 和 Linux 宿主机上运行。它提供了一套丰富的功能和管理工具，方便用户轻松创建和管理多个虚拟机。
* `VMware Fusion`：VMware Fusion 是专为 macOS 设计的 VMware type-2 hypervisor。它使 macOS 用户能够在 Mac 上运行 Windows 和其他操作系统，提供了与 VMware Workstation 类似的功能。
* `Oracle VirtualBox`：Oracle VirtualBox 是一款免费的开源 type-2 hypervisor，支持多种宿主机操作系统，如 Windows、macOS、Linux 和 Solaris。它易于使用且功能强大，适用于开发、测试和个人用途。
* `Parallels Desktop`：Parallels Desktop 是一款专为 macOS 设计的 type-2 hypervisor，使用户能够在 Mac 上运行 Windows 和其他操作系统。Parallels Desktop 以其易用性和集成 macOS 功能而受到好评。
* `Microsoft Hyper-V`：虽然 Hyper-V 主要作为 type-1 hypervisor 而知名，但在 Windows 10 Pro 和 Enterprise 版本中，它也可以作为type-2 hypervisor 使用。这允许用户在 Windows 操作系统上创建和运行虚拟机。


# Simulator
## QEMU
QEMU 是一个通用的开源处理器模拟器和虚拟机监控器（VMM）。它支持多种处理器架构，包括 x86、ARM、MIPS、PowerPC、RISC-V 等。
* QEMU 可以用作用户模式模拟器（用于运行单个目标架构的应用程序）或全系统模拟器（用于模拟整个硬件系统）。
* QEMU 提供了对多种设备和外设的模拟，从而支持更复杂的系统和软件开发。
* QEMU 通过动态二进制翻译技术提供较高的性能，但相比硬件性能仍然较低。
* QEMU 可以与 KVM 结合使用，通过硬件虚拟化技术实现接近原生性能的虚拟机运行。

## Spike
Spike 是 RISC-V 架构的一个参考模拟器，它可以模拟 RISC-V 的指令集，以及 RISC-V 的硬件架构。
* Spike 主要用于验证 RISC-V 设计以及在没有实际硬件的情况下进行软件开发。
* Spike 模拟的设备和外设较少，主要关注 RISC-V 处理器本身。
* Spike 的性能较低，因为它主要用于指令集验证和开发，而不是用于实际的应用程序执行。

## [kvmtool](https://git.kernel.org/pub/scm/linux/kernel/git/will/kvmtool.git/about/)
kvmtool 是一个轻量级的 KVM 虚拟化解决方案，它提供了一个简单的用户空间工具集，用于创建和管理 KVM 虚拟机。


## 练习
[使用Rust实现vhost-user设备](https://github.com/oscomp/proj129-vhost-user-devices-in-rust)  
[用Rust语言重写Linux kernel中的KVM](https://github.com/oscomp/proj178-kvm-in-rust)  


# 参考
[虚拟化技术发展编年史](https://zhuanlan.zhihu.com/p/27409164)  
[CentOS Cloud images](http://cloud.centos.org/centos/7/images/)  
[​[qemu][http]qemu的网络类型disk技术分析](https://cloud.tencent.com/developer/article/1087508)  
[[linux][storage]Linux存储栈](https://cloud.tencent.com/developer/article/1087520)  
[[Note] Learning KVM - implement your own kernel](https://david942j.blogspot.com/2018/10/note-learning-kvm-implement-your-own.html)  
[河马](https://www.zhihu.com/people/he-ma-31-68/posts)   
[惠伟](https://www.zhihu.com/people/huiweics/posts)  
