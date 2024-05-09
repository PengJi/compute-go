# 函数定义
```sh
function get_network_config {
    echo "sysconfig"
    return
}
# 调用函数
$(get_network_config)
```

# 使用 main
```sh
#!/usr/bin/env bash
func1(){
    #do sth
}

func2(){
    #do sth
}

main(){
    func1
    func2
}
main "$@" 
```


# 记录日志
```sh
function log {
    local prefix="[$(date +%Y-%m-%d\ %H:%M:%S)]"
    echo "${prefix} $@" >&2
}

log "INFO" "message"
```


# 校验命令是否执行成功
```sh
function check_cmd {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "error with $@" >&2
        exit $status
    fi
}
check_cmd shell_command
```


# 重试
[How do I write a retry logic in script to keep retrying to run it upto 5 times?](https://unix.stackexchange.com/questions/82598/how-do-i-write-a-retry-logic-in-script-to-keep-retrying-to-run-it-upto-5-times)
```sh
for i in 1 2 3 4 5; do
    for eth_file in $(ls /sys/class/net/*/address); do
        if [ "$1" == "$(cat $eth_file)" ]; then
            interface=$(echo $eth_file | awk -F/ '{print $5}')
            break
        fi
    done
    [[ ! -z $interface ]] && break || sleep 1
done
```


## 使用 heredocs
一种多行输入的方法。
```sh
cat>>/etc/rsyncd.conf << EOF
log file = /usr/local/logs/rsyncd.log
transfer logging = yes
log format = %t %a %m %f %b
syslog facility = local3
EOF
```
