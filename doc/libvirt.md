# [libvirt](https://gitlab.com/libvirt/libvirt)

# 安装
## 从源码安装
```bash
sudo apt -y install libgnutls-dane0 libgnutls-openssl27 libgnutls28-dev libgnutlsxx28 libnl-3-dev libnl-route-3-dev libpciaccess-dev libxml2-utils xsltproc libdevmapper-dev libyajl-dev libyajl2 libxml2-dev

git clone git@gitlab.com:libvirt/libvirt.git

cd $HOME
mkdir -p libvirt_build
cd libvirt

#  for libvirt 6.6.0 and older
mkdir build
cd build
../autogen.sh --prefix=$HOME/libvirt_build
sudo make -j$(nproc)
# make install is required only once to generate the config and log file structure
sudo make install

#  for libvirt 6.7.0 and later
$ meson build --prefix=$HOME/libvirt_build
$ ninja -C build
# ninja -C build install is required only once to generate the config and log file structure
$ sudo ninja -C build install
```

## 从 deb 包安装
```bash
sudo apt install libvirt-daemon virt-manager -y
```

[build libvirt](https://developer.ibm.com/tutorials/compiling-libvirt-and-qemu/)

## 常见错误
[启动 qemu 权限错误](https://unix.stackexchange.com/questions/471345/changing-libvirt-emulator-permission-denied)


# 一些典型的 libvirt xml
```xml
<!-- usb cdrom -->
<?xml version="1.0" encoding="utf-8"?>
<disk type="file" device="cdrom">
  <driver name="qemu" type="raw"/>
  <target dev="sdzy" bus="usb"/>
  <source file="/usr/share/smartx/images/vmtools/706dca56-06cc-4554-b74f-a686c8f973fb"/>
  <readonly/>
  <boot order='999'/>
  <address type='usb' bus='0' port='3'/>
</disk>

<!-- scsi cdrom -->
<?xml version="1.0" encoding="utf-8"?>
<disk type="file" device="cdrom">
  <driver name="qemu" type="raw"/>
  <target dev="sdzy" bus="scsi"/>
  <source file="/usr/share/smartx/images/8079ce65-0f2a-4059-bff0-2ffd4e264440"/>
  <readonly/>
  <boot order='999'/>
  <address type='drive' controller='0' bus='0' target='0' unit='2'/>
</disk>

<!-- usb disk -->
<disk type='file' device='disk'>
  <driver name='qemu' type='raw'/>
  <source file='/usr/share/smartx/images/ae5d0ad2-ee8b-4be8-a5e9-dd55f8beee62'/>
  <target dev='sdzy' bus='usb'/>
  <readonly/>
  <boot order='4'/>
  <address type='usb' bus='0' port='3'/>
</disk>
```

# 热添加设备
```bash
virsh attach-device 01d3658c-b11c-4e87-8214-512377513b31 usb_cdrom.xml --current
```

# 通过 libvirt 执行 qmp
```bash
# 使用 qmp 热添加 cdrom
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "__com.redhat_drive_add", "arguments": { "id": "usb_cdrom_fastio_drive_id", "file":"/usr/share/smartx/images/d3420652-67a2-4121-a489-7d415039395d","media":"cdrom"}}'
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "device_add", "arguments": { "driver": "usb-storage", "drive": "usb_cdrom_fastio_drive_id","bus": "usb.0", "port": "1" }}'

# 使用 hmp 热添加 cdrom
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "drive_add auto id=usb_cdrom_drive,if=none,file=/usr/share/smartx/images/d3420652-67a2-4121-a489-7d415039395d,media=cdrom" } }'
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "device_add usb-storage,id=usb_cdrom_device,drive=usb_cdrom_drive,bus=usb.0,port=2" }}'

# 使用 qmp 热删除 cdrom
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "drive_del usb_cdrom_drive" } }'
virsh qemu-monitor-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "human-monitor-command", "arguments": { "command-line": "device_del usb_cdrom_device" } }'
```

# 通过 libvirt 执行 qga
```bash
# 测试虚拟机里的qemu-guest-agent是否可用
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-ping" }'

# 查看支持的qemu-guest-agent指令
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-info" }'

# 获得网卡信息
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-network-get-interfaces" }'

# 执行命令，这是异步的，第一步会返回一个pid，假设为797，在第二步需要带上这个pid
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-exec", "arguments": { "path": "ip", "arg": [ "addr", "list" ], "capture-output": true } }'
virsh qemu-agent-command ca4152ab-b978-4594-be4f-b41bb2532146 --pretty '{ "execute": "guest-exec-status", "arguments": { "pid": 797 } }'
```

# 管理虚拟机
[管理虚拟机](https://docs.openeuler.org/zh/docs/20.03_LTS/docs/Virtualization/%E7%AE%A1%E7%90%86%E8%99%9A%E6%8B%9F%E6%9C%BA.html)

# 其他命令
dump
当虚拟机状态异常时，比如无响应，可 dump 其内存状态。
```bash
virsh dump --memory-only --live e5fb54af-98ec-46d7-a69b-5a8fb6b52996 name.dump
crash vmlinux name.dump

# 查看任务状态
virsh domjobinfo e5fb54af-98ec-46d7-a69b-5a8fb6b52996
```
[20.19. Creating a Dump File of a Guest Virtual Machine's Core Using virsh dump](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-domain_commands-creating_a_dump_file_of_a_domains_core)


# libvirt Python 接口
 ```python
import logging
import traceback

import libvirt
import libvirt_qemu

DEFAULT_CMD_TIMEOUT = 10


class LibvirtLocalConnection(object):
    def __init__(self):
        self._conn = None
        self._domain_cache = {}

    @property
    def conn(self):
        if self._conn is None:
            self._conn = libvirt.open("qemu:///system")
        return self._conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error("libvirtError (%s)%s: %s", exc_type, exc_val, "".join(traceback.format_tb(exc_tb)))
        if self._conn:
            self._conn.close()

    def execute_qemu_agent_command(self, dom_name, command_json, timeout=None):
        """Run qga command

        command reference: https://qemu-project.gitlab.io/qemu/interop/qemu-ga-ref.html
        https://github.com/libvirt/libvirt/blob/master/src/libvirt-qemu.c
        :param dom_name: vm_uuid
        :param command_json: built-in commands or scripts
        :param timeout: maximum command execution time
        :return: commands result
        """
        try:
            if timeout is None:
                timeout = DEFAULT_CMD_TIMEOUT
            if dom_name not in self._domain_cache:
                self._domain_cache[dom_name] = self.conn.lookupByName(dom_name)
            dom = self._domain_cache[dom_name]
            # The flags parameter of qemuAgentCommand is reserved for future use that must just pass 0 for now
            return libvirt_qemu.qemuAgentCommand(dom, command_json, timeout, 0)
        except libvirt.libvirtError as excp:
            raise Exception(excp.message)

    def execute_qemu_monitor_command(self, dom_name, command_josn):
        """Run QMP command

        command reference: https://qemu-project.gitlab.io/qemu/interop/qemu-qmp-ref.html
        :param dom_name: vm_uuid
        :param command_josn: qmp command
        :return: commands result
        """
        try:
            if dom_name not in self._domain_cache:
                self._domain_cache[dom_name] = self.conn.lookupByName(dom_name)
            domain = self._domain_cache[dom_name]
            return libvirt_qemu.qemuMonitorCommand(
                domain, command_josn, libvirt_qemu.VIR_DOMAIN_QEMU_MONITOR_COMMAND_DEFAULT
            )
        except libvirt.libvirtError as excp:
            raise Exception(excp.message)


if __name__ == "__main__":
    import json

    with LibvirtLocalConnection() as conn:
        vm_uuid = "ca4152ab-b978-4594-be4f-b41bb2532146"
        cdrom_iso = "/usr/share/smartx/images/d3420652-67a2-4121-a489-7d415039395d"

        agent_command_args = {"execute": "guest-info"}
        # print(conn.execute_qemu_agent_command(vm_uuid, json.dumps(agent_command_args)))

        # hotplug cdrom
        drive_args = {
            "execute": "__com.redhat_drive_add",
            "arguments": {"id": "usb_cdrom_drive", "file": cdrom_iso, "media": "cdrom"},
        }f
        add_device_args = {
            "execute": "device_add",
            "arguments": {
                "driver": "usb-storage",
                "id": "usb_cdrom_device",
                "drive": "usb_cdrom_drive",
                "bus": "usb.0",
            },
        }
        print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(drive_args)))
        print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(add_device_args)))

        # run hmp by qmp
        hmp_drive_args = {
            "execute": "human-monitor-command",
            "arguments": {
                "command-line": "drive_add auto id=usb_cdrom_drive,if=none,file={},media=cdrom".format(cdrom_iso)
            },
        }
        hmp_add_device_args = {
            "execute": "human-monitor-command",
            "arguments": {"command-line": "device_add usb-storage,id=usb_cdrom_device,drive=usb_cdrom_drive,bus=usb.0"},
        }
        # print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(hmp_drive_args)))
        # print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(hmp_add_device_args)))

        # hot detach cdrom
        del_device_args = {"execute": "device_del", "arguments": {"id": "usb_cdrom_device"}}
        # print(conn.execute_qemu_monitor_command(vm_uuid, json.dumps(del_device_args)))
 ```
