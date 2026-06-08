"""Task runner for executing scheduled jobs."""
import threading
import time
import queue
from datetime import datetime
from typing import Optional
from task import Task, TaskStatus


class TaskRunner:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.task_queue: queue.Queue = queue.Queue()
        self.running = False
        self.workers = []

    def start(self):
        self.running = True
        for _ in range(self.max_workers):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            self.workers.append(t)

    def stop(self):
        self.running = False
        for t in self.workers:
            t.join(timeout=5)

    def _worker(self):
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                self._run_task(task)
            except queue.Empty:
                continue

    def _run_task(self, task: Task):
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        try:
            task.result = f"Executed {task.func}"
            task.status = TaskStatus.SUCCESS
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
        finally:
            task.completed_at = datetime.now()

    def submit(self, task: Task):
        self.task_queue.put(task)

    def submit_func(self, name: str, func: str, args: tuple = (), kwargs: dict = None):
        task = Task(
            id=f"{name}_{int(time.time())}",
            name=name,
            func=func,
            args=args,
            kwargs=kwargs or {}
        )
        self.submit(task)
        return task
