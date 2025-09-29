常用命令示例：
```bash
iscsiadm -m discovery --op update -t sendtargets -p 10.0.18.72:3260
iscsiadm -m discovery -t sendtargets -p 10.0.18.72:3260
iscsiadm -m node --targetname iqn.2016-02.com:system:4f7269cd-cdf8-4ea6-b293-6a20d04c728d -p 10.0.18.72:3260 -l
```
