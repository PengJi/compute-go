import abc
import json
import traceback
import uuid

from backend import Backend
from broker import Broker


class BaseTask(abc.ABC):
    """
    Example Usage:
        class AdderTask(BaseTask):
            task_name = "AdderTask"
            def run(self, a, b):
                result = a + b
                return result
        adder = AdderTask()
        adder.delay(9, 34)
    """

    task_name = None

    def __init__(self):
        if not self.task_name:
            raise ValueError("task_name should be set")
        self.broker = Broker()

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """
        Derived classes must override this functions

        put your business logic here
        """
        raise NotImplementedError("Task `run` method must be implemented.")

    def update_state(self, task_id, state, meta={}):
        """
        update state
        """
        _task = {"state": state, "meta": meta}
        serialized_task = json.dumps(_task)
        backend = Backend()
        backend.enqueue(queue_name=task_id, item=serialized_task)
        print(f"task info: {task_id} succesfully queued")

    def delay(self, *args, **kwargs):
        """
        async execute
        """
        try:
            self.task_id = str(uuid.uuid4())
            _task = {"task_id": self.task_id, "args": args, "kwargs": kwargs}
            serialized_task = json.dumps(_task)
            # enqueue redis
            self.broker.enqueue(queue_name=self.task_name, item=serialized_task)
            print(f"task: {self.task_id} succesfully queued")
        except Exception:
            traceback.print_exc()
        return self.task_id

        # raise Exception("Unable to publish task to the broker.")


def async_result(task_id):
    """
    get task stat.
    You can call this function to get the execution status of the task
    """
    backend = Backend()
    _dequeued_item = backend.dequeue(queue_name=task_id)
    dequeued_item = json.loads(_dequeued_item)
    state = dequeued_item["state"]
    meta = dequeued_item["meta"]

    class Info:
        def __init__(self, state, meta):
            self.state = state
            self.meta = meta

    info = Info(state, meta)
    return info
