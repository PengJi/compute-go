# 最佳实践
1. 使用 `local` 在函数内定义局部变量，使用 `readonly` 定义全局变量；

2. 使用$()代替\`(反单引号)；
   * $()能够支持内嵌；
   * $()不用转义；

   ```sh
   echo "A-`echo B-\`echo C-\\\`echo D\\\`\``"  # out: A-B-C-D
   echo "A-$(echo B-$(echo C-$(echo D)))"  # out: A-B-C-D
   ```

3. 尽量使用 `[[]]` 来代替 `[]`；
   * 避免转义问题；
   * 有不少新功能，包括但不限于：  
   （1）|| ：逻辑or  
   （2）&& ：逻辑and  
   （3）< ：字符串比较（不需要转义）  
   （4）== ：通配符(globbing)字符串比较  
   （5）=~ ：正则表达式(regular expression, RegEx)字符串比较  

   ```sh
   [ "${name}" \> "a" -o "${name}" \< "z" ]
   [[ "${name}" > "a" && "${nmae}" < "z" ]]
   # 字符串替换
   var="abc123"
   [[ "$var" == abc* ]]  # 正则匹配，true
   [[ "$var" == "abc*" ]]  # 字面比较，false
   [[ "$var" =~ [abc]+[123]+ ]]  # 正则匹配，true
   # 注意：从bash3.2开始，通配符和正则表达式都不能用引号包裹了（所以，上面的例子，加了引号就是字面比较）。

   var="a b+"
   [[ "a bbb" =~ $var ]]
   # 如果表达式里含有空格，则必须存储到一个变量里，再进行通配符与正则比较。
   ```

4. 简单的 `if` 尽量使用` && ||` 写成单行，比如 `[[ x > 2]] && echo x`；

5. 利用 `/dev/null` 过滤不友好的输出信息；

6. 利用命令的返回值判断命令的执行情况；

7. 使用文件前要判断文件是否存在，否则做好异常处理；

8. 使用封装提高代码的可读性；
   ```sh
   function ExtractComments {
     egrep "^#"
   }
   cat test.sh | ExtractComments | wc
   ```

9. 为防止变量中含有空格，对变量使用双引号，如：`"${var}"`；

10. 使用 `mktemp` 生成临时文件或文件夹，
   参考：[mktemp 命令和 trap 命令教程](http://www.ruanyifeng.com/blog/2019/12/mktemp.html)；

11. 会使用 `trap` 捕获信号，并在接受到终止信号时执行一些收尾工作，例如：`trap 'rm -f "$TMPFILE"' EXIT`，
   参考：[trap信号捕捉用法详解](https://www.junmajinlong.com/shell/script_course/shell_trap/)；


# 指定解释器
当以 ./file.py 方式执行的时候，会从以下命令行中寻找解释器
```sh
#!/bin/bash
#!/usr/bin/env bash 
#!/usr/bin/env python
```


# 输出重定向
```sh
# 禁止输出 stdout 和 stderr
>/dev/null 2>&1

# 输出错误到标准输出
2>&1

# 重定向到 stderr
echo "error msg" >&2
```

# 字符串操作
## 字符串读取
|  表达式   | 含义  |
|  ----  | ----  |
| `${var}`  | 变量 var 的值, 与 `$var` 相同 |
| `${var-DEFAULT}`  | 如果 var 没有被声明, 那么就以 `$DEFAULT` 作为其值 |
| `${var:-DEFAULT}` | 如果 var没有被声明, 或者其值为空, 那么就以 `$DEFAULT` 作为其值 |
| `${var=DEFAULT}`	| 如果 var 没有被声明, 那么就以 `$DEFAULT` 作为其值 |
| `${var:=DEFAULT}`	| 如果 var 没有被声明, 或者其值为空, 那么就以` $DEFAULT` 作为其值 |	 
| `${var+OTHER}`	| 如果 var 声明了, 那么其值就是 `$OTHER`, 否则就为 `null` 字符串 |
| `${var:+OTHER}`	| 如果 var 被设置了, 那么其值就是 `$OTHER` , 否则就为 `null` 字符串 | 
| `${var?ERR_MSG}`	| 如果 var 没被声明, 那么就打印 `$ERR_MSG` |
| `${var:?ERR_MSG}`	| 如果 var 没被设置, 那么就打印 `$ERR_MSG` |
| `${!varprefix*}`	| 匹配之前所有以 `varprefix` 开头进行声明的变量 |
| `${!varprefix@}`	| 匹配之前所有以 `varprefix` 开头进行声明的变量 |

# 字符串操作
|  表达式   | 含义  |
|  ----  | ----  |
| `${#string}` | `$string` 的长度 |
| `${string:position}`	| 在 `$string` 中, 从位置 `$position` 开始提取子串 |
| `${string:position:length}` | 在 `$string` 中, 从位置 `$position` 开始提取长度为`$length` 的子串 |
| `${string#substring}` | 从变量 `$string` 的开头, 删除最短匹配 `$substring` 的子串
| `${string##substring}` | 从变量 `$string` 的开头, 删除最长匹配 `$substring` 的子串
| `${string%substring}` | 从变量 `$string` 的结尾, 删除最短匹配 `$substring` 的子串
| `${string%%substring}` | 从变量 `$string` 的结尾, 删除最长匹配 `$substring` 的子串
| `${string/substring/replacement}` | 使用 `$replacement` , 来代替第一个匹配的`$substring` |
| `${string//substring/replacement}` | 使用 `$replacement` 代替所有匹配的`$substring` |
| `${string/#substring/replacement}` | 如果 `$string` 的前缀匹配 `$substring`, 那么就用 `$replacement` 来代替匹配到的 `$substring` |
| `${string/%substring/replacement}` | 如果 `$string` 的后缀匹配 `$substring`, 那么就用 `$replacement` 来代替匹配到的 `$substring` |


# 逻辑运算符
```sh
"A ; B"  # Run A and then B, regardless of success of A
"A && B"  # Run B if A succeeded
"A || B"  # Run B if A failed
"A &"  # Run A in background.

false && echo howdy!
true && echo howdy!
howdy!

true || echo howdy!
false || echo howdy!
howdy!
```


# [控制 shell 执行模式](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
* `set -e`  或 `set -o errexit`

如果脚本中任意命令执行失败（具有非零的退出状态），则 bash 立即退出。  
这种行为同编程语言类似，如：python、c 等，其中任何语句执行失败，则程序立即退出，不执行后续命令。  
默认情况下，在执行脚本时若遇到错误命令，则 bash 会继续执行后面命令，整个脚本退出码是成功的，这种行为容易忽略错误。  
符合 fail fast 设计理念。
```sh
#!/bin/bash
set -e

hello  # 立即退出
echo "Hello"
```

使用 set +e 可以暂时关闭。
```sh
set +e
$(ls foobar)
set -e
```
还有一种方式能达到类似目的
`command || true`
即使执行失败，脚本也不会退出。

* `set -u` 或 `set -o nounset`

执行脚本时，除了 $* 和 $@，遇到任何未定义的变量都会报错并立即退出。  
这种行为同编程语言类似，如：python、c 等，变量必须先定义再引用。  
符合 fail fast 设计理念。
```sh
#!/usr/bin/env bash
echo $test  # 输出空

set -u
echo $hello  # 报错：hello: unbound variable
```

* `set -o pipefail`

该命令使如果管道中任何命令失败，则失败命令的返回码将作为整个管道的返回码。  
默认情况下，管道的最后一条命令是管道的返回码。

```sh
#!/usr/bin/env bash
grep some-string /non/exist/file | sort
echo $?
# grep 的错误码为 2，错误信息写入 stderr，stdout 为空，则 sort 的输入为空，可正确执行，整条命令管道的返回码为 0。

set -o pipefail

grep some-string /non/exist/file | sort
echo $?
# 整条命令管道的返回码为 2。
```

* `set -x`

将所有执行的命令都打印到终端。  
典型的用法：在执行脚本时，可以显示每个执行步骤。
```sh
#!/bin/bash
set -x

if [[ -f "/dev/sr0" ]]; then  # 输出控制流
    echo "hello"
elif [[ -f "/dev/sr1" ]]; then
    echo "hi"
else
    echo "world"
fi

# 输出：
# + [[ -f /dev/sr0 ]]
# + echo world
# world
```


# 调试
```sh
# 对脚本进行语法检查
bash -n test.sh

# 跟踪每个命令的执行
bash -v test.sh
# 或
set -o verbose

# 跟踪每个命令的执行，并附加扩充信息
bash -x test.sh
# 或
set -o xtrace
```


# 数据结构

## 字符串
### 字符串包含
```sh
if [[ "hello world" =~ "hello" ]]; then
    echo "包含"
else
    echo "不包含"
fi
```

### 分割字符串
```sh
# 第一种方式
OLD_IFS=$IFS
IFS=","
for ntp_server in $1; do
    echo $ntp_server
done
IFS=$OLD_IFS

# 第二种方式
string="hello,shell,haha"
array=(${string//,/ }) 
for var in ${array[@]}
do
  echo $var
done

# 第三种方式
string="one,two,three,four,five"
array=(`echo $string | tr ',' ' '` ) 
for var in ${array[@]}
do
  echo $var
done
```

## 数组
### 遍历数组
```sh
OLD_IFS=$IFS
IFS=","
for dns_server in ${dns_servers}; do
    tmp_dns_servers+=($dns_server)
done
IFS=$OLD_IFS
```


# 控制流
## if
```sh
if [[ -f "/etc/os-release" ]]; then
    os_type=$(cat /etc/os-release | grep PRETTY_NAME)
    if [[ ${os_type} =~ "CentOS Linux 8" ]]; then
        echo "nm"
        return
    elif [[ ${os_type} =~ "ubuntu" ]]; then
        echo "ubuntu"
        return
    else
        echo "not found"
    fi
fi

if [[ -n "${TEAM_MASTER}" ]] && [[ ! "${DEVICETYPE}" = "TeamPort" ]]; then
    ./ifup-TeamPort ${CONFIG} $2
    ethtool_set
    exit 0
fi
```

## switch
```sh
case "$(get_network_config)" in
    rhel|centos||fedora)
        by_eni $1 $2 $3 $4
        ;;
    sysconfig)
        by_sysconfig $1 $2 $3 $4
        ;;
    networkmanager)
        by_nm $1 $2 $3 $4
        ;;
    netplan)
        by_netplan $1 $2 $3 $4
        ;;
    *)
        echo "Unsupported network config system" >&2
        exit 1
        ;;
esac
```

[Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)  
规范检查：[koalaman/shellcheck](https://github.com/koalaman/shellcheck)
