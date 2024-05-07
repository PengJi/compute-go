from queue import Queue
from threading import Thread
import time


# 实现自定义线程池

queue = Queue()


class ThreadNum(Thread):
    """
    创建线程
    """
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            num = self.queue.get()
            print("retrieved ", num)

            time.sleep(1)

            self.queue.task_done()

        print("finished")


def main():
    # 创建一个 thread pool, 这里开启5个并发线程
    for i in range(5):
        t = ThreadNum(queue)
        t.setDaemon(True)
        t.start()

    # 往队列中填数据
    for num in range(10):
        queue.put(num)

    queue.join()


if __name__ == '__main__':
    main()
