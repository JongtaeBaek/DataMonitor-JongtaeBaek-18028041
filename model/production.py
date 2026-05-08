from collections import deque
from dataclasses import dataclass


@dataclass
class ProductionJob:
    order_id: str
    sample_id: str
    required_quantity: int
    actual_production: int
    total_time: float


class ProductionQueue:
    def __init__(self):
        self._queue: deque[ProductionJob] = deque()

    def enqueue(self, job: ProductionJob):
        self._queue.append(job)

    def dequeue(self) -> ProductionJob | None:
        return self._queue.popleft() if self._queue else None

    def peek(self) -> ProductionJob | None:
        return self._queue[0] if self._queue else None

    def all(self) -> list[ProductionJob]:
        return list(self._queue)

    def is_empty(self) -> bool:
        return len(self._queue) == 0
