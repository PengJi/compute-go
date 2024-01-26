将 vmlinuz 转为 vmlinux
```bash
dd if=./{vmlinuz} skip=`grep -a -b -o -m 1 -e $'\x1f\x8b\x08\x00' ./{vmlinuz} | cut -d: -f 1` bs=1 | zcat > ./{vmlinux}
```
