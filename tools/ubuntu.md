备份
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

# 软件
forticlient
[https://repo.fortinet.com/](https://repo.fortinet.com/)


