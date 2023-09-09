一些典型的 libvirt xml
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

热添加设备
```bash
virsh attach-device 01d3658c-b11c-4e87-8214-512377513b31 usb_cdrom.xml --current
```

通过 libvirt 执行 qmp
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

通过 libvirt 执行 qga
```bash
# 测试虚拟机里的qemu-guest-agent是否可用
virsh qemu-agent-command DOMAIN --pretty '{ "execute": "guest-ping" }'

# 查看支持的qemu-guest-agent指令
virsh qemu-agent-command DOMAIN --pretty '{ "execute": "guest-info" }'

# 获得网卡信息
virsh qemu-agent-command DOMAIN --pretty '{ "execute": "guest-network-get-interfaces" }'

# 执行命令，这是异步的，第一步会返回一个pid，假设为797，在第二步需要带上这个pid
virsh qemu-agent-command DOMAIN --pretty '{ "execute": "guest-exec", "arguments": { "path": "ip", "arg": [ "addr", "list" ], "capture-output": true } }'
virsh qemu-agent-command DOMAIN --pretty '{ "execute": "guest-exec-status", "arguments": { "pid": 797 } }'
```

 libvirt Python 接口
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
