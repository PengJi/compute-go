命令行启动 qemu
```sh
/usr/libexec/qemu-kvm -name guest=187306a8-5cfb-4d2d-967b-a23d7714b087,debug-threads=on \
-cpu host -m size=4194304k,slots=255,maxmem=4194304000k -realtime mlock=off -smp 4,maxcpus=240,sockets=240,cores=1,threads=1 \
-device piix3-usb-uhci,id=usb,bus=pci.0,addr=0x1.0x2 \
-device nec-usb-xhci,p2=15,p3=15,id=usb1,bus=pci.0,addr=0x5 \
-device usb-ehci,id=usb2,bus=pci.0,addr=0x6 \
-device piix3-usb-uhci,id=usb3,bus=pci.0,addr=0x7 \
-drive file.driver=iscsi,file.portal=127.0.0.1:3260,file.target=iqn.2016-02.com.smartx:system:zbs-iscsi-datastore-1637755567369y,file.lun=127,file.transport=tcp,format=raw,if=none,id=drive-virtio-disk0,cache=none,aio=native \
-device virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=drive-virtio-disk0,id=virtio-disk0,bootindex=1,write-cache=on \
-drive file=/usr/share/smartx/images/ae5d0ad2-ee8b-4be8-a5e9-dd55f8beee62,file.locking=off,format=raw,if=none,id=drive-ide0-0-0,readonly=on \
-device ide-cd,bus=ide.0,unit=0,drive=drive-ide0-0-0,id=ide0-0-0,bootindex=2 \
-vnc 192.168.74.83:5 \
-monitor stdio \
-chardev socket,id=qmp,port=4444,host=localhost,server \
-mon chardev=qmp,mode=control,pretty=on
```
参数
`-vnc`           指定 vnc 地址和端口，可使用 vnc viewer 连接，比如：192.168.74.83:5
`-monitor stdio` 在启动 qemu 之后，进入交互式命令行，可执行 hmp 命令
`-chardev -mon`  通过 tcp 与 qemu 交互，可执行 qmp 命令

若要添加 `cdrom` 驱动器和设备，可在命令行添加如下参数
```sh
-device virtio-scsi-pci,id=scsi0 \
-drive id=cdrom0,if=none,format=raw,readonly=on,file=/usr/share/smartx/images/ae5d0ad2-ee8b-4be8-a5e9-dd55f8beee62 \
-device scsi-cd,bus=scsi0.0,drive=cdrom0
```

