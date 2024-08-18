工具技术

# 使用 http 传输文件
在主机 B 拷贝主机 A 的文件
## 主机A
在一个 terminal 中开启 server
```bash
python -m http.server 80
```

在另一个 terminal
```bash
function gscp() {
    file_name=$1
    if [ -z "$file_name" ]; then
    echo $0 file
    return 1
    fi

    ip_addr=$(ip a | grep -v vir | grep -o "192\..*" | cut -d/ -f1)
    file_path=$(readlink -f $file_name)
    echo run: scp -r $(whoami)@${ip_addr}:$file_path .
}

gscp $1
```

## 主机B
```bash
scp -r $(whoami)@${ip_addr}:${file_path}
```
