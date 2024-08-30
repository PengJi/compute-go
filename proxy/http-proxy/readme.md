auth server
172.26.23.163(本地)
```bash
# 在本地启动 auth server
cd auth-server
go run main.go
# 产生 token
python client.py
```

file server
192.168.35.140
```bash
# 启动 file server
cd file-server
go run main.go
```

proxy server
192.168.35.141
```bash
# 启动 proxy server
cd proxy-server
go run main.go
```

# 调用 client，修改 token
```bash
python client.py
```
