# grep
搜索目标行和前后 10 行
`grep -10 dd.txt`

避免出现一些不可预知的问题使用 `-w`
`grep -w "a sentence" txt`

***

# sed
## 参数
`-i`  修改当前文件   
`-e`  支持执行更丰富的语法，比如脚本  

## 动作：替换字符
`s` 替换文本中的字符，可以使用正则表达式
```sh
# 将 `/dev/sd` 替换为 `/dev/vd`，使用 `#` 当作标识符 
sed "s#/dev/sd#/dev/vd#g" /etc/fstab
```

## 动作：替换行
`c` c 后面的字符串可以替换 n1,n2 之前的行
```bash
sed '2,5c No 2-5 number' file  # 将第 2-5 行的内容取代成为 No 2-5 number
```

## 动作：插入
`i` i 后面的字符串会插入匹配行的上一行 
```bash
sed '2i drink tea' file  # 在第 2 行前添加新行（加在第 2 行）
```

## 动作：新增
`a` 在匹配行的下一行添加新行
```bash
sed '2a drink tea' file  # 在第 2 行后添加新行（加在第 3 行）

sed '2a Drink tea or ......\
drink beer ?' file  # 添加两行
```

## 动作：打印
`p` 打印匹配的行
```bash
sed -n '5,7p' file  # 打印第 5-7 行
```

## 动作：删除
`d` 可删除特定的行
```sh
# 删除匹配行
sed '/%cdrom_caption%/d' /tmp/file

# 删除文件第一行
sed '1d' sed-demo.txt

# 删除文件最后一行
sed '$d' sed-demo.txt

# 删除指定行（第3行）
sed '3d' sed-demo.txt

# 删除指定范围内的行
sed '5,7d' sed-demo.txt  # 删除第 5 到 7 行
sed '1d;5d;9d;$d' sed-demo.txt  # 删除第 1 行、第 5 行、第 9 行和最后一行
sed '3,$d' sed-demo.txt  # 删除第 3 行到最后一行

# 删除指定范围以外的行（第 3 到 6 行范围以外的所有行）
sed '3,6!d' sed-demo.txt

# 删除空行
sed '/^$/d' sed-demo.txt

# 删除包含某个模式的行
sed '/System/d' sed-demo.txt  # 删除匹配到 System 模式的行

# 删除包含字符串集合中某个字符串的行
sed '/System\|Linux/d' sed-demo.txt  # 删除匹配到 System 或 Linux 表达式的行

# 以指定字符开头的行
sed '/^R/d' sed-demo-1.txt  # 删除以 R 字符开头的所有行
sed '/^[RF]/d' sed-demo-1.txt  # 删除 R 或者 F 字符开头的所有行

# 删除以指定字符结尾的行
sed '/m$/d' sed-demo.txt  # 删除 m 字符结尾的所有行
sed '/[xm]$/d' sed-demo.txt  # 删除 x 或者 m 字符结尾的所有行

# 删除所有大写字母开头的行
sed '/^[A-Z]/d' sed-demo-1.txt  # 删除所有大写字母开头的行

# 删除指定范围内匹配模式的行
sed '1,6 {/Linux/d;}' sed-demo.txt  # 删除第 1 到 6 行中包含 Linux 表达式的行

# 删除匹配模式的行及其下一行
sed '/System/ {N;d;}' sed-demo.txt  # 删除包含 System 表达式的行以及它的下一行

# 删除包含数字的行
sed '/[0-9]/d' sed-demo.txt  # 删除所有包含数字的行
sed '/^[0-9]/d' sed-demo.txt  # 删除所有以数字开头的行
sed '/[0-9]$/d' sed-demo.txt  # 删除所有以数字结尾的行

# 删除包含字母的行
sed '/[A-Za-z]/d' sed-demo.txt  # 删除所有包含字母的行
```

## 数据查找并执行动作
```bash
sed -n '/oo/,/pp/ {/text/d; p; q}' file  # 匹配包含 oo 和 pp 之间的行，并删除包含 text 的行
```

## 正则表达式匹配
* `^` 匹配行首  
`sed -n '/^start/ p' file`

* `$` 匹配行尾   
`sed -n '/end$/ p' file`

* `.` 匹配任意单个字符  
`sed -n '/^.at$/p' file`  
`.at` 匹配 `bat`、`cat`、`mat` 等等，但是不能匹配 `at` 或 `ccat` 等

* `[]` 匹配任意存在字符列表中的一个字符  
`sed -n '/[CT]all/ p' file`  
`[CT]` 可以匹配单个 `C` 或 `T` ，但是不能匹配其它字符，也不能匹配 `CT`

* `[^]` 匹配任意不在字符列表中的一个字符  
`sed -n '/[^CT]all/ p' file`  
`[^CT]` 可以任意单个字符，除了 `C` 或 `T`

* `[-]` 匹配连续范围的字符  
`sed -n '/[C-Z]all/ p' file`    
`[C-Z]` 表示任意单个存在字符列表 `[CDEFGHIJKLMNOPQRSTUVWXYZ]` 里的字符

* `\?` 只出现 0 次或 1 次  
`sed -n '/Pea\?r/ p' file`  
`Pea\?r` 可以匹配 `Per` 或 `Pear`，但不能匹配 `Peaar`

* `\+` 至少出现一次  
`sed -n '/Pea\+r/ p' file`  
`Pea\+r` 可以匹配 `Pear` 或 `Peaar`，但不能匹配 `Per`

* `*` 出现任意次数  
`sed -n '/ca*t/ p' file`  
`ca*t` 可以匹配 `ct`、`cat` 或 `caat` 等等

* `{n}` 精确出现 n 次  
`sed -n '/^8\{3\}$/ p' file`  
`^8\{3\}$` 只能匹配 `888` 而不能匹配 `88` 或 `8888`

* `{n,}`  至少出现 n 次  
`sed -n '/^8\{3,\}$/ p' file`  
`^8\{3,\}$` 可以匹配 `888` 或 `8888` 但不能匹配 `88`

* `{m, n}` 出现 M 到 N 次  
`sed -n '/^8\{3,\}$/ p' file`  
`^8{2,4}$` 可以匹配 `88`、`888`、`8888` 但是不会匹配 `8` 和 `88888`

参考  
[sed 正则表达式](https://www.twle.cn/c/yufei/sed/sed-basic-regular-expressions.html)

***

# awk
获取最后一列
`awk -F',' '{print $NF}'`

获取倒数第二列
`awk '{print $(NF-1)}'`


# 正则表达式
示例：有效的电话号码，格式为 `(xxx) xxx-xxxx` 或 `xxx-xxx-xxxx`（x 表示一个数字），比如：
```sh
987-123-4567  # 有效
123 456 7890  # 无效
(123) 456-7890  # 有效
```
shell 
```sh
grep -P '^([0-9]{3}-|\([0-9]{3}\) )[0-9]{3}-[0-9]{4}$' file.txt

awk '/^([0-9]{3}-|\([0-9]{3}\) )[0-9]{3}-[0-9]{4}$/' file.txt
```