ThreadPoolExecutor 不仅可以自动调度线程，还可以：
（1）主线程可以获取某一个线程（或者任务的）的状态，以及返回值；  
（2）当一个线程完成的时候，主线程能够立即知道；
（3）让多线程和多进程的编码接口一致；

下面是 ThreadPoolExecutor 的使用方法。
1. 使用 ThreadPoolExecutor 来实例化线程池对象。传入 `max_workers` 参数来设置线程池中最多能同时运行的线程数目。
```py
from concurrent.futures import ThreadPoolExecutor
import time
 
def get_html(times):
    time.sleep(times)
    print("get page {} success".format(times))
    return times
 
executor = ThreadPoolExecutor(max_workers=2)    # 表示在这个线程池中同时运行的线程有3个线程
```

2.  使用 `submit` 函数来提交线程需要执行的任务（函数名和参数）到线程池中，并返回该任务的句柄（类似于文件、画图），注意 submit() 不是阻塞的，而是立即返回。  
通过 submit 函数返回的任务句柄，能够使用 `done()` 方法判断任务是否结束。
```py
from concurrent.futures import ThreadPoolExecutor,as_completed

def doFileParse(filepath,segment,wordslist):
   print(filepath)
   print(segment)

#调用方法
args =[filepath,thu1,Words]
newTask=executor.submit(lambda p: doFileParse(*p),args)
```

3. 使用 `cancel()` 方法可以取消提交的任务，如果任务已经在线程池中运行了，就取消不了。这个例子中，线程池的大小设置为2，任务已经在运行了，会取消失败。如果改变线程池的大小为1，那么先提交的是task1，task2还在排队等候，这是时候就可以成功取消。

4. 使用 `result()` 方法可以获取任务的返回值，这个方法是阻塞的。
```py
#通过submit函数提交执行的函数到线程池中, submit 是立即返回
task1 = executor.submit(get_html, (3))    # 第一个是回调函数，第二个是传给函数的参数
task2 = executor.submit(get_html, (2))    
 
#done方法用于判定某个任务是否完成
print(task1.done())
 
# cancel方法用于取消某个任务
print(task2.cancel())
 
# result方法可以获取task的执行结果, 这个方法是阻塞的
print(task1.result())
```

5. `as_completed()` 方法，上面虽然提供了判断任务是否结束的方法，但是不能在主线程中一直判断，有时候我们是得知某个任务结束了，就去获取结果，而不是一直判断每个任务有没有结束。这是就可以使用 `as_completed()` 方法一次取出所有任务的结果。
as_completed() 方法是一个生成器，在没有任务完成的时候，会阻塞，在有某个任务完成的时候，会 yield 这个任务，就能执行for循环下面的语句，然后继续阻塞住，循环到所有的任务结束。从结果也可以看出，先完成的任务会先通知主线程。
```py
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
 
# 参数times用来模拟网络请求的时间
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times
 
executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 4] # 并不是真的url
all_task = [executor.submit(get_html, (url)) for url in urls]
 
for future in as_completed(all_task):
    data = future.result()
    print("in main: get page {}s success".format(data))
 
"""
执行结果
get page 2s finished
in main: get page 2s success
get page 3s finished
in main: get page 3s success
get page 4s finished
in main: get page 4s success
"""
```

6. 使用 `map` 方法，无需提前使用 submit 方法，map 方法与 python 标准库中的 map 含义相同，都是将序列中的每个元素都执行同一个函数，下面的代码就是对 urls 的每个元素都执行 get_html 函数，并分配到线程池里。可以看到执行结果与上面的 as_completed 方法的结果不同，输出顺序和 urls 列表的顺序相同，就算 2s 的任务先执行完成，也会先打印出3s的任务先完成，再打印2s的任务完成。
```py
import time
from concurrent.futures import ThreadPoolExecutor
 
def get_html(times):
    time.sleep(times)
    print("get page {} success".format(times))
    return times
 
executor = ThreadPoolExecutor(max_workers=2) 
 
# 通过executor的 map 获取已经完成的task的值
for data in executor.map(get_html, urls):
    print("get {} page".format(data))
```

7. `wait` 方法可以让主线程阻塞，直到满足设定的要求。wait 方法接收3个参数，等待的任务序列、超时时间以及等待条件。等待条件 reture_when 默认为 `ALL_COMPLETED`，表明要等待所有的任务都结束。可以看到运行结果中，确实是所有任务都完成了，主线程才打印出 main。等待条件还可以设置为 `FIRST_COMPLETED`，表示第一个任务完成就停止等待。
```py
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import time
 
# 参数times用来模拟网络请求的时间
def get_html(times):
    time.sleep(times)
    print("get page {}s finished".format(times))
    return times
 
executor = ThreadPoolExecutor(max_workers=2)
urls = [3, 2, 4] # 并不是真的url
all_task = [executor.submit(get_html, (url)) for url in urls]
wait(all_task, return_when=ALL_COMPLETED)
print("main")

# 执行结果 
# get page 2s finished
# get page 3s finished
# get page 4s finished
# main
```

使用示例
```python
from concurrent import futures

changed_vm_uuids = []
with futures.ThreadPoolExecutor(max_workers=10) as executor:
    res_vms = [
        executor.submit(self.delete_vm_snapshot, vm_uuid) for vm_uuid in vm_uuids
    ]
    try:
        for f in futures.as_completed(res_vms, timeout=60):
            try:
                result = f.result()
                if result is not None:
                    changed_vm_uuids.append(result)
            except Exception as excp:
                logging.error("Failed to delete snapshot, error: {}".format(excp))
    except futures.TimeoutError:
        logging.error("Failed to create VM snapshots, timeout")
        executor.shutdown(wait=False, cancel_futures=True)
return changed_vm_uuids
```

[https://blog.csdn.net/xiaoyu_wu/article/details/102820384](https://blog.csdn.net/xiaoyu_wu/article/details/102820384)  
[https://www.jianshu.com/p/b9b3d66aa0be](https://www.jianshu.com/p/b9b3d66aa0be)  
