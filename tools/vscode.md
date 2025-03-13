# 配置
代码字体大小：在配置中搜 font
侧边栏字体大小：在配置中搜 zoomLevel

# EXTENSIONS

## python
python 代码静态检查：flake8、pylance、ruff
```shell
"python.linting.enabled": true,
"python.linting.pycodestyleEnabled": false,
"python.linting.flake8Enabled": true,
"python.linting.flake8Args": [
    "--max-line-length=120",
    "--ignore=C901"
],
```

python 代码格式化：black
```shell
"python.formatting.provider": "black",
"python.formatting.blackArgs": [
    "--line-length=120"
],
```

## clang
代码格式化： `clang-format`
```shell
.clang-format

BasedOnStyle: Google
AccessModifierOffset: -4
IndentWidth: 4
ColumnLimit: 0
```
[Clang-Format Style Options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)

## rust
[ruff rules](https://beta.ruff.rs/docs/rules/#mccabe-c90)  

## go
`golangci-lint`
全局配置：`~/.golangci.yml`
[安装配置](https://www.superpig.win/blog/details/ujoiykoy)
[linter](https://golangci-lint.run/usage/configuration/)

# vscode 实用快捷键
打开最近的项目
`ctrl + r`

打开左侧边栏
`ctrl + b`

打开右侧边栏
`alt + ctrl + b`

# AI代码插件
通义灵码
1. 智能补全

1.1 行级/函数级实时补全

操作  macos   Windows
接受行间代码建议    `Tab` `Tab`
废弃行间代码建议    `esc` `esc`
查看上一个行间推荐结果 `(option) [`   `Alt [`
查看下一个行间推荐结果 `(option) ]`    `Alt ]`
手动触发行间代码建议  `(option) P`  `Alt P`

1.2 自然语言生成代码

2. 代码问答
2.1 当对某段代码有疑问或期望针对代码进行一些问题解决时，选中代码后，在智能问答窗口的输入框中输入问题。

2.2 `@workspace`本地工程问答
当需要快速了解一个工程、查找工程内的实现逻辑，或有新的诉求需要进行代码变更时，可以在智能问答窗口中通过 @ 可唤起 `@workspace`，
选中后输入问题或诉求，通义灵码可快速结合当前仓库进行工程理解、代码查询、代码问答等，同时可以通过自然语言描述需求，
结合当前工程生成简单需求或缺陷的整体修改建议和相关建议代码。

2.3 `@terminal`问答
当遇到执行指令不知道如何写，或者不清楚某个指令的意思时，可以在智能问答窗口中通过 @ 可唤起 `@terminal`，
选择后使用自然语言描述需要指令诉求，通义灵码将可以生成你需要的命令。生成指令后，可以一键插入到 teminal 中进行执行或让通义灵码继续解释。
当然，也可以在选择 `@terminal` 后，输入指令让通义灵码生成指令解释。

2.4 清空会话上下文历史记忆
当在会话中时，在智能问答输入框中输入 / 即可看到 `/clear context` 指令，选择后即可清空当前会话的上下文历史记忆。
