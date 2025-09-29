在 `*nix` 中，可以使用 `fork` 创建子进程，子进程与父进程异步运行。
当子进程运行结束后，内核会释放其占用的资源比如：占用的内存，打开的问文件等，但内核会保留一些信息，比如：进程号、退出状态等，以便于父进程通过 `wait/waitpid` 查询子进程的状态并释放保留的信息。  
子进程与父进程运行结束时间不同。若父进程先退出，子进程运行，则子进程会变为孤儿进程。若子进程先退出，父进程运行，则子进程会变为僵尸进程，等待父进程调用 `wait/waitpid`。

## 孤儿进程
* 若父进程退出，它的子进程还在运行，则这些子进程将成为孤儿进程。
* 孤儿进程将被1号进程（init 或者 systemd）托管，从而成为1号进程的子进程，所以孤儿进程没有危害。

示例
```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>

int main()
{
    pid_t pid;
    pid = fork();  // create new process
    if (pid < 0) {
        perror("fork error:");
        exit(1);
    }

    if (pid == 0) {  // child process
        printf("I am the child process %d.\n", getpid());
        printf("child process pid: %d ppid: %d\n", getpid(), getppid());
        printf("child process will sleep 5s.\n");

        sleep(5);  // wait parent process to exit

        // child proces become orphan process, parent child pid is 1.
        printf("child process pid: %d ppid: %d\n", getpid(), getppid());
        printf("child process is exited.\n");
    } else {
        printf("I am parent process %d.\n", getpid());
        sleep(1);
        printf("parent process is exited.\n");
    }
    return 0;
}
```
输出
```s
I am parent process 1815267.
I am the child process 1815268.
child process pid: 1815268 ppid: 1815267
child process will sleep 5s.
parent process is exited.

child process pid: 1815268 ppid: 1
child process is exited.
```

## 僵尸进程
* 子进程退出，父进程并没有调用 `wait` 或者 `waitpid` 释放子进程的资源（进程号，退出状态、运行时间等），这些资源就一直存在系统中，子进程就会成为僵尸进程。
* 任何一个子进程在 exit 之后，都会经历僵尸进程的阶段，如果父进程一直没有调用 `wait/waitpid` 处理，则在系统中的状态会一直是 Z(Zombie)。
* 如果父进程一直没有调用 `wait/waitpid`，则其进程的保留信息便一直不会被释放，进程号就会被一直占用，而系统的进程号是有限的，所以可能导致无法创建新进程。

示例  
产生一个僵尸进程
```c
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>

int main()
{
    pid_t pid;
    pid = fork();
    if (pid < 0) {
        perror("fork error:");
        exit(1);
    }

    if (pid == 0) {  // child process
        printf("I am child process. I am exiting.\n");
        exit(0);
    }

    printf("I am parent process. I will sleep two seconds\n");

    sleep(2);  // wait child to exit

    // show process state, will have a zombie process
    system("ps -o pid,ppid,state,tty,command");

    printf("parent process is exiting.\n");
    return 0;
}
```
输出
```s
I am parent process. I will sleep two seconds
I am child process. I am exiting.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1819495 1807412 S pts/11   ./a.out
1819496 1819495 Z pts/11   [a.out] <defunct>
1819508 1819495 R pts/11   ps -o pid,ppid,state,tty,command
parent process is exiting.
```
产生一个僵尸进程，状态为 Z。


示例  
产生多个僵尸进程
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

int main()
{
    pid_t  pid;
    while (1) {
        pid = fork();
        if (pid < 0) {
            perror("fork error:");
            exit(1);
        }

        if (pid == 0) {
            printf("I am a child process. I am exiting.\n");
            exit(0);
        } else {
            sleep(10);

            system("ps -o pid,ppid,state,tty,command");

            continue;
        }
    }
    return 0;
}
```
输出
```s
I am a child process. I am exiting.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1823357 1807412 S pts/11   ./a.out
1823358 1823357 Z pts/11   [a.out] <defunct>
1823439 1823357 R pts/11   ps -o pid,ppid,state,tty,command
I am a child process. I am exiting.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1823357 1807412 S pts/11   ./a.out
1823358 1823357 Z pts/11   [a.out] <defunct>
1823446 1823357 Z pts/11   [a.out] <defunct>
1823514 1823357 R pts/11   ps -o pid,ppid,state,tty,command
I am a child process. I am exiting.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1823357 1807412 S pts/11   ./a.out
1823358 1823357 Z pts/11   [a.out] <defunct>
1823446 1823357 Z pts/11   [a.out] <defunct>
1823515 1823357 Z pts/11   [a.out] <defunct>
1823637 1823357 R pts/11   ps -o pid,ppid,state,tty,command
I am a child process. I am exiting.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1823357 1807412 S pts/11   ./a.out
1823358 1823357 Z pts/11   [a.out] <defunct>
1823446 1823357 Z pts/11   [a.out] <defunct>
1823515 1823357 Z pts/11   [a.out] <defunct>
1823638 1823357 Z pts/11   [a.out] <defunct>
1823768 1823357 R pts/11   ps -o pid,ppid,state,tty,command
I am a child process. I am exiting.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1823357 1807412 S pts/11   ./a.out
1823358 1823357 Z pts/11   [a.out] <defunct>
1823446 1823357 Z pts/11   [a.out] <defunct>
1823515 1823357 Z pts/11   [a.out] <defunct>
1823638 1823357 Z pts/11   [a.out] <defunct>
1823769 1823357 Z pts/11   [a.out] <defunct>
1823853 1823357 R pts/11   ps -o pid,ppid,state,tty,command
```
可以看到每次循环都会有一个僵尸进程产生。

### 避免产生僵尸进程的方法
（1）子进程退出想父进程发送 `SIGCHILD` 信号，父进程在信号处理函数中调用 `wait`。

以下三个条件会产生 `SIGCHILD` 信号：
1. 子进程终止时
2. 子进程接收到 `SIGSTOP`信号停止时
3. 子进程处在停止态，接受到 `SIGCONT` 后唤醒时

示例
```c
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>

static void sig_child(int signo)
{
     pid_t        pid;
     int        stat;
     while ((pid = waitpid(-1, &stat, WNOHANG)) >0)
            printf("child %d terminated.\n", pid);
}

int main()
{
    pid_t pid;

    signal(SIGCHLD, sig_child);

    pid = fork();
    if (pid < 0) {
        perror("fork error:");
        exit(1);
    }

    if (pid == 0) {
        printf("I am child process, pid id %d. I am exiting.\n",getpid());
        exit(0);
    }

    printf("I am parent process.\n");
    sleep(2);

    system("ps -o pid,ppid,state,tty,command");

    printf("parent process is exiting.\n");
    return 0;
}
```
输出
```s
I am parent process.
I am child process, pid id 1887670. I am exiting.
child 1887670 terminated.
    PID    PPID S TT       COMMAND
1807412 1807405 S pts/11   -bash
1887669 1807412 S pts/11   ./a.out
1887671 1887669 R pts/11   ps -o pid,ppid,state,tty,command
father process is exiting.
```

（2）fork 两次  
使子进程成为孤儿进程，从而让其父进程变为1号进程，1号进程就可以僵尸进程。
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

int main()
{
    pid_t  pid;
    pid = fork();
    if (pid < 0) {
        perror("fork error:");
        exit(1);
    }

    // first child process
    if (pid == 0) {
        printf("I am the first child process pid: %d ppid: %d\n", getpid(), getppid());

        pid = fork();
        if (pid < 0) {
            perror("fork error:");
            exit(1);
        }

        // first child process exit
        if (pid >0) {
            printf("first procee is exited.\n");
            exit(0);
        }

        // second child process 
        sleep(3);
        printf("I am the second child process pid: %d ppid:%d\n", getpid(), getppid());
        exit(0);
    }

    // waitpid for first child(already exit)
    if (waitpid(pid, NULL, 0) != pid) {
        perror("waitepid error:");
        exit(1);
    }

    exit(0);
    return 0;
}
```
