# 启动 file server
192.168.35.140
```bash
# 启动 file server
cd file-server
go run main.go
```

# 启动 proxy server
192.168.35.141
```bash
sudo systemctl start nginx
```

# 获取 token
auth server
172.26.23.163(本地)
```bash
# 在本地启动 auth server
cd auth-server
go run main.go

# 产生 token
python auth_client.py -g | python -m json.tool
```

# 上传文件
```bash
python client.py -u -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDk5MDE5MCwidXNlcm5hbWUiOiJ0ZXN0In0.wMZ2o-B4w3qK6yoXumrp_o7SMGzLUXv2whGVIk5vLkY
```

# 下载文件
```bash
python client.py -d -t eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIiwiY2x1c3RlcklkIjoiMCIsImV4cCI6MTcyNDk5MDE5MCwidXNlcm5hbWUiOiJ0ZXN0In0.wMZ2o-B4w3qK6yoXumrp_o7SMGzLUXv2whGVIk5vLkY
```
