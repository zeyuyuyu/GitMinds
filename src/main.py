from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import heapq

@dataclass
class Task:
    id: str
    title: str
    priority: int
    due_date: Optional[datetime]
    tags: List[str]
    completion_status: bool = False

class TaskPrioritizer:
    def __init__(self):
        self.tasks: List[Task] = []
        self.priority_queue = []
        self.tag_weights: Dict[str, float] = {}
    
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self._update_priority_queue()
    
    def complete_task(self, task_id: str) -> None:
        for task in self.tasks:
            if task.id == task_id:
                task.completion_status = True
                self._update_priority_queue()
                break
    
    def _calculate_dynamic_priority(self, task: Task) -> float:
        if task.completion_status:
            return float('-inf')
        
        base_priority = task.priority
        
        # Factor in due date
        if task.due_date:
            time_until_due = (task.due_date - datetime.now()).total_seconds()
            if time_until_due > 0:
                urgency_factor = 100000 / (time_until_due + 1)
                base_priority += urgency_factor
        
        # Factor in tag weights
        tag_priority = sum(self.tag_weights.get(tag, 0) for tag in task.tags)
        
        return base_priority + tag_priority
    
    def _update_priority_queue(self) -> None:
        self.priority_queue = []
        for task in self.tasks:
            if not task.completion_status:
                priority = self._calculate_dynamic_priority(task)
                heapq.heappush(self.priority_queue, (-priority, task.id, task))
    
    def get_next_tasks(self, n: int = 5) -> List[Task]:
        result = []
        temp_queue = self.priority_queue.copy()
        
        while temp_queue and len(result) < n:
            _, _, task = heapq.heappop(temp_queue)
            if not task.completion_status:
                result.append(task)
        
        return result
    
    def update_tag_weight(self, tag: str, weight: float) -> None:
        self.tag_weights[tag] = weight
        self._update_priority_queue()

def main():
    prioritizer = TaskPrioritizer()
    
    # Example usage
    task1 = Task(
        id="1",
        title="Implement core features",
        priority=5,
        due_date=datetime(2024, 1, 1),
        tags=["development", "critical"]
    )
    
    prioritizer.add_task(task1)
    prioritizer.update_tag_weight("critical", 2.0)
    
    next_tasks = prioritizer.get_next_tasks()
    for task in next_tasks:
        print(f"Next task: {task.title} (Priority: {task.priority})")

if __name__ == "__main__":
    main()