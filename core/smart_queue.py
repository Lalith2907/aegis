from collections import deque
from enum import Enum

class Decision(Enum):
    ACCEPT = "ACCEPT"
    WAIT = "WAIT"
    REJECT = "REJECT"

class SmartQueue:
    def __init__(self, max_workers: int, max_queue_size: int):
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.active_workers = 0
        self.queue = deque()

    def admit_request(self, request_id: str, priority: str) -> Decision:
        if self.active_workers < self.max_workers:
            self.active_workers += 1
            print(f"[ACCEPT] Request {request_id} accepted immediately")
            return Decision.ACCEPT
        
        if len(self.queue) < self.max_queue_size:
            self.queue.append((request_id, priority))
            print(f"[WAIT] Request {request_id} queued")
            return Decision.WAIT
        
        if priority.upper() == "HIGH":
            self.queue.append((request_id, priority))
            print(f"[WAIT] High priority request {request_id} queued")
            return Decision.WAIT
        
        else:
            print(f"[REJECT] Low priority request {request_id} rejected")
            return Decision.REJECT