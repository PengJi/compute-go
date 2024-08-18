from app import LongTask
from worker import Worker

if __name__ == "__main__":
    # Start the process to execute task
    long_task = LongTask()
    worker = Worker(task=long_task)

    worker.start()
