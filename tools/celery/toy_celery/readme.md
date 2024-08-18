# 实现简单 celery
## 步骤
1. 实现任务类 task.py
定义了 BaseTask 类，它继承自 python 的 `abc.ABC` 成为一个抽象基类，其中一开始便要求必须定义 task_name，这是因为后面我们需要通过 task_name 去找对应的任务队列。  
BaseTask 类的 `run()` 方法被 `abc.abstractmethod` 装饰，该装饰器会要求 BaseTask 的派生类必须重写 run() 方法，这是为了让使用者可以自定义自己的任务逻辑。  
BaseTask 类的 `update_state()` 方法用于更新任务的状态，其逻辑很简单，先将参数进行JSON序列化，然后调用 Backend 的 `enqueue()` 方法将数据存入，这里的 Backend 其实是 Redis 实例，`enqueue()` 方法会将数据写入 Redis 的 list 中，需要注意，这里 list 的 key 为 task_id，即当前任务的id。  
BaseTask类的 `delay()` 方法用于异步执行任务，首先通过 uuid 为任务创建一个唯一id，然后将方法的参数通过JSON序列化，然后调用 Broker 的 `enqueue()` 将数据存入，这里的 Broker 其实也是一个 Redis 实例，`enqueue()` 方法同样是将数据写入到 Redis 的 list 中，只是 list 的 key 为 task_name，即当前任务的名称。  
还实现了 `async_result()` 方法，该方法用于异步获取任务的数据，通过该方法可以获得任务的执行结果，或任务执行中的各种数据，数据的结构是有简单约定的，必须要有 state 表示当然任务的状态，必须要有 meta 表示当前任务的一些信息。

2. 实现 Broker 与 Backend
在 task.py 中使用了 Broker 与 Backend。  
定了两个方法用于数据的存储与读取，存储使用 `lpush` 方法，它会将数据从左边插入到 Redis 的 list 中，读取数据使用 brpop 方法，它会从 list 的右边取出第一个元素，返回该元素值并从 list 删除，左进右出就构成了一个队列。

3. 后台任务执行进程 Worker
定义了 Worker 类， Worker 类在初始化时需要指定具体的任务实例，然后从 broker 中获取任务相关的数据，接着调用其中的 `run()` 方法完成任务的执行。

4. 定义一个耗时任务
每个耗时任务都要继承在 BaseTask 并且重写其 `run()` 方法，`run()` 方法中的逻辑就是当前这个耗时任务要处理的具体逻辑。  
在for迭代中，想要前端知道当前任务for迭代的具体情况，就需要将相应的数据通过BaseTask的 `update_state()` 方法将其更新到 backend 中，使用 task_id 作为 Redis 中 list 的 key。  
当逻辑全部执行完后，将状态为 FINISH 的信息存入 backend 中。  

## running steps
1. intall redis  
`brew install redis`
   
2. start redis  
`redis-server`
   
3. start flask  
`python app.py`
   
4. start worker  
`python run_worker.py`  
It equivalent to execute `celery -A xxx worker --loglevel=info`
   
5. start task
`http://127.0.0.1:5000/`

# references
[动手实现一个简单的Celery](https://juejin.cn/post/6844903957312045064)  
[ayuLiao/toy_celery](https://github.com/ayuLiao/toy_celery)
