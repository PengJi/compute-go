# 多级目录切换

## `cd -`
`cd -` 中的`-` 就相当于变量 `$OLDPWD`。`cd -` 就相当于 `cd $OLDPWD`。
```sh
$ pwd
/dir/a

$ cd /dir/b
$ echo $OLDPWD
/dir/a

$ cd $OLDPWD
$ pwd
/dir/a
```

pushd 和 popd 是对一个目录栈进行操作，目录栈以栈结构保存目录，栈顶永远存放着当前目录。  
dirs 显示目录栈的内容。

## `dirs` 
`-p`  以行显示目录栈，每行一个目录
`-v`  以行显示目录栈，同时显示每一个目录在栈中的索引
`-c`  清空目录栈

```sh
$ pwd
/root/vmtools-agent/svt

$ dirs
~/vmtools-agent/svt ~/vmtools-agent ~

$ dirs -p
~/vmtools-agent/svt
~/vmtools-agent
~

$ dirs -v
 0  ~/vmtools-agent/svt
 1  ~/vmtools-agent
 2  ~
```


## `pushd`

* pushd
将目录栈最顶层的两个目录进行交换。相当于 `cd -`。
```sh
$ dirs -p
~/vmtools-agent/svt
~/vmtools-agent
~

$ pushd
~/vmtools-agent ~/vmtools-agent/svt ~

$ dirs -p
~/vmtools-agent
~/vmtools-agent/svt
~
```

* pushd {dir}
将 {dir} 压入栈顶，并当前目录为 {dir}，

```sh
$ pushd rpm
~/vmtools-agent/rpm ~/vmtools-agent ~/vmtools-agent/svt ~

$ dirs -p
~/vmtools-agent/rpm
~/vmtools-agent
~/vmtools-agent/svt
~
```

* pushd +n
切换到栈中的任意一个目录。
`pushd +n` 切换到目录栈中的第 n 个目录（n 为使用 `dirs -v`显示的索引），即将该目录以循环的方式移到栈顶。
`+n` 从栈顶向栈底的第 n 个元素。
`-n` 从栈底向栈顶的第 n 个目录。

```sh
$ dirs -v
 0  ~/vmtools-agent/rpm
 1  ~/vmtools-agent
 2  ~/vmtools-agent/svt
 3  ~

$ pushd +2
~/vmtools-agent/svt ~ ~/vmtools-agent/rpm ~/vmtools-agent

$ dirs -v
 0  ~/vmtools-agent/svt  # 其余目录循环上移
 1  ~
 2  ~/vmtools-agent/rpm
 3  ~/vmtools-agent
```

## `popd`

* popd
将目录栈中栈顶元素出栈。此时栈顶元素发生变化，当前目录切换。

```sh
$ dirs -v
 0  ~/vmtools-agent/svt
 1  ~
 2  ~/vmtools-agent/rpm
 3  ~/vmtools-agent

$ popd
~ ~/vmtools-agent/rpm ~/vmtools-agent

$ dirs -v
 0  ~
 1  ~/vmtools-agent/rpm
 2  ~/vmtools-agent
 ```

* popd +n
将目录栈中的第 n 个元素删除。

```sh
$ dirs -v
 0  ~
 1  ~/vmtools-agent/rpm
 2  ~/vmtools-agent

$ popd +1
~ ~/vmtools-agent

$ dirs -v
 0  ~
 1  ~/vmtools-agent
```
