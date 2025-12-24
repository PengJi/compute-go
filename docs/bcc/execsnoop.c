// 引入内核头文件
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/fs.h>

// 定义sys_enter_execve跟踪点处理函数.
TRACEPOINT_PROBE(syscalls, sys_enter_execve)
{
    // 变量定义
    unsigned int ret = 0;
    const char **argv = (const char **)(args->argv);

    // 获取进程PID和进程名称
    struct data_t data = { };
    u32 pid = bpf_get_current_pid_tgid();
    data.pid = pid;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    // 获取第一个参数（即可执行文件的名字）
    if (__bpf_read_arg_str(&data, (const char *)argv[0]) < 0) {
        goto out;
    }

    // 获取其他参数（限定最多5个）
    #pragma unrollfor (int i = 1; i < TOTAL_MAX_ARGS; i++) {
        if (__bpf_read_arg_str(&data, (const char *)argv[i]) < 0) {
            goto out;
        }
    }

 out:
    // 存储到哈希映射中
    tasks.update(&pid, &data);
    return 0;
}

// 定义sys_exit_execve跟踪点处理函数.
TRACEPOINT_PROBE(syscalls, sys_exit_execve)
{
    // 从哈希映射中查询进程基本信息
    u32 pid = bpf_get_current_pid_tgid();
    struct data_t *data = tasks.lookup(&pid);

    // 填充返回值并提交到性能事件映射中
    if (data != NULL) {
        data->retval = args->ret;
        events.perf_submit(args, data, sizeof(struct data_t));

        // 最后清理进程信息
        tasks.delete(&pid);
    }

    return 0;
}
