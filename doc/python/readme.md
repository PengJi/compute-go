Python

# 读取大文件
## 逐行读取
```python
with open('filename', 'r', encoding = 'utf-8') as f:
    while True:
        line = f.readline()  # 逐行读取
        if not line:  # 到 EOF，返回空字符串，则终止循环
            break
        do_something(line)
```

## 分块读取
```python
def read_in_chunks(file_obj, chunk_size = 2048):
    """
    逐件读取文件
    默认块大小：2KB
    """
    while True:
        data = file_obj.read(chunk_size)  # 每次读取指定的长度
        if not data:
            break
        yield data

with open('filename', 'r', encoding = 'utf-8') as f:
    for chuck in read_in_chunks(f):
        do_something(chunk)

```

## pythonic 方式
```python
with open('filename', 'r', encoding = 'utf-8') as f:
    for line in f:
        do_something(line)
```

[Python——读取大文件（GB）](https://www.cnblogs.com/yuanfang0903/p/11433491.html)
