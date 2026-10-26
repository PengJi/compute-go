# 删除模块缓存
```bash
# 删除 /golang.org/x/tools@v0.45.0
rm -rf $(go env GOMODCACHE)/cache/download/golang.org/x/tools
sudo rm -rf "$(go env GOMODCACHE)/golang.org/x/tools@v0.45.0" 
```
