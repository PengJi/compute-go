基于 9p 协议在虚拟机和宿主机之间共享文件
（1）在宿主机上创建目录和文件
```sh
root@kvm:~# mkdir /tmp/shared
root@kvm:~# touch /tmp/shared/file
```
（2）使用 libvirt 编辑 domain
```sh
root@kvm:~# virsh edit kvm1
 ...
 <devices>
   ...
   <filesystem type='mount' accessmode='passthrough'>
     <source dir='/tmp/shared'/>
     <target dir='tmp_shared'/>
   </filesystem>
   ...
 </devices>
 ...
Domain kvm1 XML configuration edited.
```
（3）启动虚拟机并连接控制台
```sh
root@kvm:~# virsh start kvm1
Domain kvm1 started

root@kvm:~# virsh console kvm1
Connected to domain kvm1
Escape character is ^]

Debian GNU/Linux 8 debian ttyS0

debian login: root
Password:
...
```
（4）确保9p和virtio内存驱动已经加载
```sh
root@debian:~# lsmod | grep 9p
9pnet_virtio 17006 0
9pnet 61632 1 9pnet_virtio
virtio_ring 17513 3 virtio_pci,virtio_balloon,9pnet_virtio
virtio 13058 3 virtio_pci,virtio_balloon,9pnet_virtio
```
（5）挂载共享目录并查看文件
```sh
root@debian:~# mount -t 9p -o trans=virtio tmp_shared /mnt
root@debian:~# mount | grep tmp_shared
tmp_shared on /mnt type 9p (rw,relatime,sync,dirsync,trans=virtio)
root@debian:~# ls -la /mnt/
total 8
drwxr-xr-x 2  root root 4096 Mar 23 11:25 .
drwxr-xr-x 22 root root 4096 Mar 22 16:28 ..
-rw-r--r-- 1  root root 0    Mar 23 11:25 file
```