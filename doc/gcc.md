在Ubuntu中切换GCC版本，可以通过安装多个GCC版本并使用`update-alternatives`工具来管理不同版本之间的切换。以下是切换GCC版本的步骤：

### 1. 安装额外的GCC版本

首先，确保你已经安装了需要的GCC版本。你可以通过APT包管理器来安装：

```bash
sudo apt update
sudo apt install gcc-9 g++-9  # 以安装GCC 9为例
```

安装其它版本，只需将命令中的版本号改为所需版本即可。

### 2. 设置`update-alternatives`

使用`update-alternatives`配置GCC。这允许你在多个版本之间切换。

```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9
```

这个命令设置了GCC 9作为可选择的一个版本。`90`是优先级，如果你有多个版本，确保每个版本的优先级不同。`--slave`标志同时设置了相应版本的G++。

为其他版本重复这个过程，比如：

```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 80 --slave /usr/bin/g++ g++ /usr/bin/g++-8
```

### 3. 切换GCC版本

使用下面的命令切换到你希望使用的GCC版本：

```bash
sudo update-alternatives --config gcc
```

系统将列出所有已安装的GCC版本，并让你选择使用哪一个版本。

### 4. 验证切换

使用以下命令验证当前正在使用的GCC版本：

```bash
gcc --version
```

### 注意事项

- 确保安装了所有需要的版本的GCC和G++，因为它们通常是成对使用的。
- 使用不同版本的GCC可能需要不同版本的库。在编译大型项目或特定软件时，请注意依赖项。
- 在更改GCC版本时，特别是在系统级别上，要小心，因为这可能会影响到依赖特定版本编译器的其他软件。