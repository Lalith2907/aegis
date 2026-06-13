from enum import Enum
from core.sqs_client import send_to_queue, get_queue_depth
from core.cloudwatch_client import publish_metric

class Decision(Enum):
    ACCEPT = "ACCEPT"
    WAIT = "WAIT"
    REJECT = "REJECT"

class SmartQueue:
    def __init__(self, max_workers: int, max_queue_size: int):
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.active_workers = 0
        self.total_requests = 0
        self.accepted_requests = 0
        self.queued_requests = 0
        self.rejected_requests = 0

    def admit_request(self, request_id: str, priority: str) -> Decision:
        self.total_requests += 1
        if self.active_workers < self.max_workers:
            self.active_workers += 1
            self.accepted_requests += 1
            publish_metric("AcceptedRequests", self.accepted_requests)
            publish_metric("ActiveWorkers", self.active_workers)
            print(f"[ACCEPT] Request {request_id} accepted immediately")
            return Decision.ACCEPT

        try:
            current_queue_depth = get_queue_depth()
        except Exception as e:
            print(f"[ERROR] Unable to get queue depth: {e}")
            return Decision.REJECT
        if current_queue_depth < self.max_queue_size:
            self.queued_requests += 1
            publish_metric("QueuedRequests", self.queued_requests)
            publish_metric("QueueDepth", current_queue_depth + 1)
            send_to_queue(request_id, priority)
            print(f"[WAIT] Request {request_id} queued in SQS")
            return Decision.WAIT

        if priority.upper() == "HIGH":
            self.queued_requests += 1
            publish_metric("QueuedRequests", self.queued_requests)
            publish_metric("QueueDepth", current_queue_depth + 1)
            send_to_queue(request_id, priority)
            print(f"[WAIT] High priority request {request_id} queued in SQS")
            return Decision.WAIT
        
        self.rejected_requests += 1
        publish_metric("RejectedRequests", self.rejected_requests)
        print(f"[REJECT] Low priority request {request_id} rejected")
        return Decision.REJECT

    def on_worker_complete(self):
        if self.active_workers == 0:
            return
        self.active_workers -= 1
        publish_metric("ActiveWorkers", self.active_workers)
        print(f"[INFO] Worker completed. Active workers: {self.active_workers}")
        
    def get_state(self):
        return {
            "active_workers": self.active_workers,
            "queue_depth": get_queue_depth(),
            "max_workers": self.max_workers,
            "max_queue_depth": self.max_queue_size,
            "total_requests": self.total_requests,
            "accepted_requests": self.accepted_requests,
            "queued_requests": self.queued_requests,
            "rejected_requests": self.rejected_requests
        }