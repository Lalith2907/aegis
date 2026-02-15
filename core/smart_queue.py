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

        self.total_requests = 0
        self.accepted_requests = 0
        self.queued_requests = 0
        self.rejected_requests = 0

    def admit_request(self, request_id: str, priority: str) -> Decision:
        self.total_requests += 1
        if self.active_workers < self.max_workers:
            self.active_workers += 1
            self.accepted_requests += 1
            print(f"[ACCEPT] Request {request_id} accepted immediately")
            return Decision.ACCEPT
        
        if len(self.queue) < self.max_queue_size:
            self.queued_requests += 1
            self.queue.append((request_id, priority))
            print(f"[WAIT] Request {request_id} queued")
            return Decision.WAIT
        
        if priority.upper() == "HIGH":
            self.queued_requests += 1
            self.queue.append((request_id, priority))
            print(f"[WAIT] High priority request {request_id} queued")
            return Decision.WAIT
        
        else:
            self.rejected_requests += 1
            print(f"[REJECT] Low priority request {request_id} rejected")
            return Decision.REJECT

    def on_worker_complete(self):
        if self.active_workers == 0:
            return
        
        self.active_workers -= 1
        print(f"[INFO] Worker completed. Active workers: ", self.active_workers)

        if self.queue:
            request_id, priority = self.queue.popleft()
            self.active_workers += 1
            print(f"[DEQUEUE] Request {request_id} taken from queue and assigned to worker")

    def get_state(self):
        return {
            "active_workers": self.active_workers,
            "queue_depth": len(self.queue),
            "max_workers": self.max_workers,
            "max_queue_depth": self.max_queue_size,
            "total_requests": self.total_requests,
            "accepted_requests": self.accepted_requests,
            "queued_requests": self.queued_requests,
            "rejected_requests": self.rejected_requests
        }