# 删除模块缓存
```bash
# 删除 cps-common@v1.67.2
rm -rf $(go env GOMODCACHE)/cache/download/gitlab.ctyuncdn.cn/esx/cps/cps-common
sudo rm -rf "$(go env GOMODCACHE)/gitlab.ctyuncdn.cn/esx/cps/cps-common@v1.67.2" 
```
