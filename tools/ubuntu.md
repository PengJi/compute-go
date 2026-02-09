# 备份
```bash
mkdir /backups
tar cvpzf /backups/system.img --exclude=/proc --exclude=/lost+found --exclude=/mnt --exclude=/media --exclude=/sys --exclude=/tmp /
```
在备份命令结束时你可能会看到这样一个提示：’tar: Error exit delayed from previous errors’，多数情况下可以忽略它。

恢复系统文件
```bash
# optionly
rm -rf /usr /var /opt /media /home /etc /srv /sbin /root /boot /lost+found
# restore
tar xvpfz /backups/system.img -C /
# mkdir directories not in backups
sudo mkdir /proc /lost+found /mnt /sys /media /tmp
# update grub
update-grub2
# restart
reboot
```
如果原来的Ubuntu系统已经崩溃，无法进入。则可以使用Ubuntu安装U盘（live USB）进入试用Ubuntu界面。

# 配置休眠
在 Ubuntu 24.04 中，由于内核与硬件兼容性原因，休眠功能默认是关闭的。要启用它，需确保 Swap 空间大于等于物理内存，并配置引导加载程序。
1. 确认前置条件
关闭 Secure Boot：在 BIOS 中禁用它。开启此功能通常会阻止系统从休眠中恢复。
准备 Swap：确保你的 Swap 分区或文件至少与物理内存大小一致。 
[如何增加Ubuntu上的Swap大小？](https://cloud.tencent.com/developer/article/2323470)

2. 核心配置步骤（Swap 文件方式）
如果你使用的是默认的 Swap 文件（通常为 /swap.img），请按以下步骤操作：
(1) 获取 UUID	
`findmnt -no SOURCE,UUID -T /swap.img`
记录根分区的 UUID

(2) 获取 Offset	
`sudo filefrag -v /swap.img | grep " 0:" | awk '{print $4}'`
获取首个物理块号（Offset），去掉末尾的点号

(3) 修改 GRUB	
`sudo vim /etc/default/grub`
在 GRUB_CMDLINE_LINUX_DEFAULT 中添加：
resume=UUID=[你的UUID] resume_offset=[你的Offset]

示例：
```sh
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=6cefb30a-bbbc-4484-bd64-865ba7078cee resume_offset=243146752"
```

(4) 更新引导	
`sudo update-grub`
应用 GRUB 配置
   
(5) 修改 Initramfs	
`sudo vim /etc/initramfs-tools/conf.d/resume`
写入：resume=UUID=[你的UUID] resume_offset=[你的Offset]

示例：
`resume=UUID=6cefb30a-bbbc-4484-bd64-865ba7078cee resume_offset=243146752`

(6) 更新内核映射	
`sudo update-initramfs -u`	
更新启动镜像

(7) 测试休眠
保存好所有文档，执行以下命令：
`sudo systemctl hibernate`
请谨慎使用此类代码。

如果电脑关机并在重启后恢复了之前的窗口，说明配置成功。 


## 在电源菜单添加“休眠”按钮
要启用电源菜单中的休眠按钮，需要在 /etc/polkit-1/rules.d/10-enable-hibernate.rules 文件中添加相应的 Polkit 规则配置，然后重启系统. 
```sh
sudo vim /etc/polkit-1/rules.d/10-enable-hibernate.rules

polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.login1.hibernate" ||
        action.id == "org.freedesktop.login1.hibernate-multiple-sessions")
    {
        return polkit.Result.YES;
    }
});
```
GNOME 桌面用户可能还需要安装 Hibernate Status Button extension 以便直接显示休眠选项。
`sudo apt install gnome-shell-extension-manager`
然后安装 `Hibernate Status Button`

## 配置合盖休眠：
打开终端，输入 sudo vim /etc/systemd/logind.conf。
找到 #HandleLidSwitch=suspend。
取消注释（删除 #），并修改为 HandleLidSwitch=hibernate。
按 Ctrl+O 保存，Enter 确认，Ctrl+X 退出。


# 软件源
[debian 软件源](https://mirrors.tuna.tsinghua.edu.cn/help/debian/)
[ubuntu 软件仓库](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)


# 输入法
fcitx5-configtool
fcitx5-diagnose
sudo fcitx-config-gtk3
