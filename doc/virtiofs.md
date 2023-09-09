Virtio-fs（Virtio 文件系统）是一种用于在虚拟环境中共享文件系统的技术。它允许宿主机操作系统与虚拟机（VM）之间以更高效、安全且一致的方式共享文件和目录。适用于虚拟化环境中的文件共享、数据交换和存储资源管理。

Virtio-fs 的主要用途如下：
* 性能：Virtio-fs 通过提供与本地文件系统相似的性能和语义，实现了虚拟机与宿主机之间文件系统的高效共享。这对于那些对性能和应用程序兼容性有要求的场景特别重要。
* 便捷性：Virtio-fs 使得在虚拟机与宿主机之间实时共享文件和目录变得更加简单。这比通过网络复制文件在虚拟机和宿主机之间传输要方便且高效得多。
* 安全性：Virtio-fs 提供了一种安全的方法来共享宿主机上的文件系统资源，而不需要将整个磁盘或底层存储系统暴露给虚拟机。这有助于提高虚拟环境的安全性。
* 跨平台：Virtio-fs 支持多种虚拟化平台和操作系统，包括 KVM、QEMU 和 Linux。这使得 Virtio-fs 成为在不同环境中共享文件系统的通用解决方案。

Virtiofs 通过 FUSE（Filesystem in Userspace）实现，并支持 DAX（Direct Access）技术。
* 主机端（宿主机）
主机端负责运行 Virtiofs 文件系统守护程序（virtiofsd）。virtiofsd 在主机端为客户机提供文件系统访问，并处理来自客户机的文件系统请求。此外，virtiofsd 使用 FUSE 库将客户机的请求转发给主机文件系统。
* 客户机端（虚拟机）
客户机端运行一个名为 virtio_fs.ko 的内核模块，它充当 FUSE 客户端。该模块通过 VirtIO 设备与主机端的 virtiofsd 进程通信。这种通信是基于 VirtIO 通信协议的，因此具有很高的性能。客户机端的文件系统操作通过该模块传递到主机端进行处理。
* VirtIO 设备
VirtIO 设备作为主机端和客户机端之间的通信桥梁。客户机端的 virtio_fs.ko 模块和主机端的 virtiofsd 进程通过 VirtIO 设备交换消息和数据。
* FUSE
Virtiofs 使用 FUSE（Filesystem in Userspace）技术在用户空间实现文件系统操作。这种方法可以提供灵活性和安全性，因为在主机上的文件系统操作是在用户空间进行的，而不是在内核空间。
* DAX（Direct Access）
Virtiofs 支持 DAX 技术，它允许客户机直接访问主机的内存，从而提高文件访问速度。通过 DAX，客户机可以绕过内核缓冲区和文件系统层，直接访问主机内存中的数据。这种方法可以显著提高 I/O 性能。

使用的步骤示例
```sh
(host)# virtiofsd --socket-path=/tmp/vhost-fs.sock -o source=/path/to/shared/dir
(host)$ qemu -chardev socket,id=char0,path=/tmp/vhost-fs.sock -device vhost-user-fs-pci,chardev=char0,tag=myfs

(guest)# mount -t virtiofs myfs /mnt
```


[virtio-fs: A Shared File System for Virtual Machines slide](https://static.sched.com/hosted_files/kvmforum2019/ff/virtio-fs_%20A%20Shared%20File%20System%20for%20Virtual%20Machines.pdf)  
[virtio-fs: A Shared File System for Virtual Machines video](https://www.youtube.com/watch?v=969sXbNX01U)  
[Towards High-availability for Virtio-fs slide](https://static.sched.com/hosted_files/kvmforum2021/58/virtiofs_ha_jiachen.pdf)  

