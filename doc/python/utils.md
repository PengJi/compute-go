# convert nanoseconds to human-readable
```py
>>> from datetime import datetime
>>> dt = datetime.fromtimestamp(1360287003083988472 / 1000000000)
>>> dt
datetime.datetime(2013, 2, 7, 17, 30, 3)

>>> s = dt.strftime('%Y-%m-%d %H:%M:%S')
>>> s
'2013-02-07 17:30:03'

>>> s += '.' + str(int(1360287003083988472 % 1000000000)).zfill(9)
>>> s
'2013-02-07 17:30:03.083988472'

>>> dt.strftime('%Y-%m-%dT%H:%M:%S.%f')
'2013-02-07T17:30:03.083988'
```

# calculate elapsed time
```py 
import monotonic
start_time = monotonic.monotonic()
elapsed_time = int(monotonic.monotonic() - start_time)
```

# 读取大文件
## 逐行读取
```python
with open('filename', 'r', encoding = 'utf-8') as f:
    while True:
        line = f.readline()  # 逐行读取
        if not line:  # 到 EOF，返回空字符串，则终止循环
            break
        do_something(line)
```

## 分块读取
```python
def read_in_chunks(file_obj, chunk_size = 2048):
    """
    逐件读取文件
    默认块大小：2KB
    """
    while True:
        data = file_obj.read(chunk_size)  # 每次读取指定的长度
        if not data:
            break
        yield data

with open('filename', 'r', encoding = 'utf-8') as f:
    for chuck in read_in_chunks(f):
        do_something(chunk)

```

## pythonic 方式
```python
with open('filename', 'r', encoding = 'utf-8') as f:
    for line in f:
        do_something(line)
```

[Python——读取大文件（GB）](https://www.cnblogs.com/yuanfang0903/p/11433491.html)


# 实现单例模式
```python
def singleton(cls):
    """单例类装饰器"""
    instances = {}

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class President:
    pass
```

# 记录函数执行时间的装饰器
```python
from time import time


def record_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f'{func.__name__}执行时间: {time() - start}秒')
        return result
        
    return wrapper
```

# 带参数的装饰器
```python
def retry_on_grpc_error(retry_times=1):
    def _call_func(func):
        @functools.wraps(func)
        def _func(self, *args, **kwargs):
            times = 0
            while True:
                try:
                    return func(self, *args, **kwargs)
                except grpc.RpcError as excp:
                    logging.warning("exception times: %d" % times)
                    if times < retry_times:
                        times += 1
                    else:
                        logging.error("call grpc {} error: {}".format(func.__name__, str(excp)))
                        raise

        return _func

    return _call_func
```

# 使用多线程
```python
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    res_vms = [executor.submit(cls(vm_uuid, conn).update_mount_points_info) for vm_uuid in vm_uuids]
    timeout = 10
    try:
        for f in futures.as_completed(res_vms, timeout=timeout):
            result = f.result()
            if result is not None:
                changed_vm_uuids.append(result)
    except futures.TimeoutError:
        logging.warning("Timeout error")
        executor.shutdown(cancel_futures=True)
```

# 手动创建线程池
```python
import threading
import queue
import time

class Worker(threading.Thread):
    """ 工作线程，不断从任务队列中获取任务并执行 """
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.daemon = True  # 设置为守护线程，主线程退出时能够自动结束

    def run(self):
        while True:
            # 从任务队列中获取任务
            func, args, kwargs = self.task_queue.get()
            if func is None:
                # None 用来通知线程退出
                self.task_queue.task_done()
                break
            # 执行任务并将结果放入结果队列
            result = func(*args, **kwargs)
            self.task_queue.task_done()
            self.result_queue.put(result)

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = queue.Queue()
        self.results = queue.Queue()
        self.workers = [Worker(self.tasks, self.results) for _ in range(num_threads)]
        for worker in self.workers:
            worker.start()

    def submit(self, func, *args, **kwargs):
        """ 提交任务到线程池 """
        self.tasks.put((func, args, kwargs))

    def get_result(self):
        """ 获取任务结果 """
        return self.results.get()

    def close(self):
        """ 通知所有线程退出 """
        for _ in self.workers:
            self.submit(None, None, None)  # None 作为特殊任务，告知线程退出
        for worker in self.workers:
            worker.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def task(x):
    time.sleep(2)  # 模拟耗时任务
    return x * x

# 使用线程池
with ThreadPool(3) as pool:
    for i in range(5):
        pool.submit(task, i)
    for _ in range(5):
        print(pool.get_result())

```

# namedtuple的用法和作用。
命名元组与普通元组一样是不可变容器，一旦将数据存储在namedtuple的顶层属性中，数据就不能再修改了，也就意味着对象上的所有属性都遵循“一次写入，多次读取”的原则。和普通元组不同的是，命名元组中的数据有访问名称，可以通过名称而不是索引来获取保存的数据，不仅在操作上更加简单，代码的可读性也会更好。
```python
from collections import namedtuple

Card = namedtuple('Card', ('suite', 'face'))
card1 = Card('aa', 13)
card2 = Card('bb', 5)
print(f'{card1.suite}{card1.face}')
print(f'{card2.suite}{card2.face}')
>
aa12
bb5
```
