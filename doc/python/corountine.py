# -*- coding: utf-8 -*-

import asyncio

# Python3 协程使用


async def worker_1():
    print('worker_1 start')
    await asyncio.sleep(1)
    print('worker_1 done')


async def worker_2():
    print('worker_2 start')
    await asyncio.sleep(2)
    print('worker_2 done')


async def main():
    task1 = asyncio.create_task(worker_1())
    task2 = asyncio.create_task(worker_2())
    print('before await')
    await task1
    print('awaited worker_1')
    await task2
    print('awaited worker_2')


# In plain Python (≥3.7)
# %time asyncio.run(main())

# In jupyter
await main()


########## 输出 ##########

# before await
# worker_1 start
# worker_2 start
# worker_1 done
# awaited worker_1
# worker_2 done
# awaited worker_2
# Wall time: 2.01 s


# 执行过程如下：
# 1. asyncio.run(main())，程序进入 main() 函数，事件循环开启；
# 2. task1 和 task2 任务被创建，并进入事件循环等待运行；
# 3. 运行到 print，输出 'before await'；
# 4. await task1 执行，用户选择从当前的主任务中切出，事件调度器开始调度 worker_1；
# 5. worker_1 开始运行，运行 print 输出'worker_1 start'，然后运行到 await asyncio.sleep(1)， 从当前任务切出，事件调度器开始调度 worker_2；
# 6. worker_2 开始运行，运行 print 输出 'worker_2 start'，然后运行 await asyncio.sleep(2) 从当前任务切出；
# 7. 以上所有事件的运行时间，都应该在 1ms 到 10ms 之间，甚至可能更短，事件调度器从这个时候开始暂停调度；
# 8. 一秒钟后，worker_1 的 sleep 完成，事件调度器将控制权重新传给 task_1，输出 'worker_1 done'，task_1 完成任务，从事件循环中退出；
# 9. await task1 完成，事件调度器将控制器传给主任务，输出 'awaited worker_1'，·然后在 await task2 处继续等待；
# 10. 两秒钟后，worker_2 的 sleep 完成，事件调度器将控制权重新传给 task_2，输出 'worker_2 done'，task_2 完成任务，从事件循环中退出；
# 9. 主任务输出 'awaited worker_2'，协程全任务结束，事件循环结束。
