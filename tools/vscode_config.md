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
代码格式化： clang-format
```shell
.clang-format

BasedOnStyle: Google
AccessModifierOffset: -4
IndentWidth: 4
ColumnLimit: 0
```
[Clang-Format Style Options](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)


# rust
[ruff rules](https://beta.ruff.rs/docs/rules/#mccabe-c90)  
