import json


class Worker:
    """
    Example Usage:
        task = AdderTask()
        worker = Worker(task=task)
        worker.start()
    """

    def __init__(self, task) -> None:
        self.task = task

    def start(self):
        while True:
            try:
                _dequeued_item = self.task.broker.dequeue(queue_name=self.task.task_name)
                dequeued_item = json.loads(_dequeued_item)
                task_id = dequeued_item["task_id"]
                task_args = dequeued_item["args"]
                task_kwargs = dequeued_item["kwargs"]
                task_kwargs["task_id"] = task_id
                self.task.run(*task_args, **task_kwargs)
                print("succesful run of task: {}".format(task_id))
            except Exception:
                print("Unable to execute task.")
                continue
