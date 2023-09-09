# virtio-serial

# virtio-sock
[virtio-vsock Zero-configuration host/guest communication](https://vmsplice.net/~stefan/stefanha-kvm-forum-2015.pdf)  
[VSOCK: VM ↔ host socket with minimal configuration](https://static.sched.com/hosted_files/devconfcz2020a/b1/DevConf.CZ_2020_vsock_v1.1.pdf)   
[Linux内核AF_VSOCK套接字条件竞争漏洞（CVE-2021-26708）分析](https://mp.weixin.qq.com/s/WMFkPJOd29yOiGoC92QFJA)  
[Features/VirtioVsock](https://wiki.qemu.org/Features/VirtioVsock)  
[vsock(7) — Linux manual page](https://man7.org/linux/man-pages/man7/vsock.7.html)  
[Linux vsock internals](https://terenceli.github.io/%E6%8A%80%E6%9C%AF/2020/04/18/vsock-internals)


# VMCI
[VMCI Sockets Programming Guide](https://vdc-download.vmware.com/vmwb-repository/dcr-public/e104af6c-8221-42aa-9bc0-e5a9915fd812/091479af-de1e-4c03-b49a-fb60b89ed2af/ws9_esx55_vmci_sockets.pdf)  


# virtual-chip


# 网络


# 自定义实现
在 VMM 层实现一个虚拟设备，在 guest 内部通过这个虚拟设备向渲染程序发送数据。虚拟设备通通过 IPC 方式与负责渲染的程序进行通信。
