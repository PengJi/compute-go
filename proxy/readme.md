auth server
172.26.23.163

file server
192.168.35.140

proxy server
192.168.35.141

```bash
# 启动 file server
cd file-server
go run main.go

# 启动 proxy server
cd proxy-server
go run main.go

# 在本地启动 auth server
cd auth-server
go run main.go
# 产生 token
python client.py

# 调用 client，修改 token
python client.py
```
