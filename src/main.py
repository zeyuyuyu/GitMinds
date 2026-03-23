import asyncio
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
from enum import Enum
from datetime import datetime
import heapq

class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass(order=True)
class ScheduledTask:
    priority: TaskPriority
    timestamp: datetime
    task: Callable
    args: tuple = ()
    kwargs: Dict[str, Any] = None
    name: str = ''
    
    def __post_init__(self):
        self.kwargs = self.kwargs or {}

class TaskScheduler:
    def __init__(self):
        self._task_queue: List[ScheduledTask] = []
        self._running = False

    async def add_task(self, 
                      task: Callable,
                      priority: TaskPriority = TaskPriority.MEDIUM,
                      *args,
                      **kwargs) -> None:
        scheduled_task = ScheduledTask(
            priority=priority,
            timestamp=datetime.now(),
            task=task,
            args=args,
            kwargs=kwargs,
            name=task.__name__
        )
        heapq.heappush(self._task_queue, scheduled_task)

    async def run(self):
        self._running = True
        while self._running and self._task_queue:
            next_task = heapq.heappop(self._task_queue)
            try:
                if asyncio.iscoroutinefunction(next_task.task):
                    await next_task.task(*next_task.args, **next_task.kwargs)
                else:
                    next_task.task(*next_task.args, **next_task.kwargs)
            except Exception as e:
                print(f'Error executing task {next_task.name}: {str(e)}')

    def stop(self):
        self._running = False

# Example usage
async def main():
    scheduler = TaskScheduler()
    
    async def high_priority_task(msg: str):
        print(f'High priority task: {msg}')
        await asyncio.sleep(1)

    def low_priority_task(msg: str):
        print(f'Low priority task: {msg}')

    # Add tasks with different priorities
    await scheduler.add_task(
        high_priority_task,
        TaskPriority.HIGH,
        'Important work'
    )
    await scheduler.add_task(
        low_priority_task,
        TaskPriority.LOW,
        'Background work'
    )

    # Run the scheduler
    await scheduler.run()

if __name__ == '__main__':
    asyncio.run(main())