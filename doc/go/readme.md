安装  
[Download and install](https://go.dev/doc/install)

开启 modules
```sh
go env -w GO111MODULE=on
```

设置代理
```sh
go env -w GOPROXY=https://goproxy.cn,direct
```

# 代码 linter
`golangci-lint`
```shell
# 查看支持的 linter
golangci-lint linters

# 指定目录或文件
golangci-lint run dir1 dir2/... file.go

# 运行默认检查，在项目根目录运行
golangci-lint run

# 列出所有问题
golangci-lint run --out-format=colored-line-number

# 某些 linter 支持自动修复问题。运行以下命令尝试修复
golangci-lint run --fix

# 在代码中添加注释，忽略特定问题
//nolint:golint,unused
var x int
```

`staticcheck`


`gosec`
[https://github.com/securego/gosec](https://github.com/securego/gosec)  
全局配置： `~/.gosec.yaml`

常用命令
递归检查当前项目
`gosec ./...`

指定规则
`gosec -include=G101,G103,G106,G108,G112,G113,G114,G601,G602 ./...`

忽略规则
`gosec -exclude=G303 ./...`

输出检测结果到文件
`gosec -fmt=json -out=results.json ./...`
