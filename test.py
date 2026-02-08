from core.smart_queue import SmartQueue, Decision

sq = SmartQueue(max_workers=2, max_queue_size=3)

requests = [
    ("r1", "LOW"),
    ("r2", "LOW"),
    ("r3", "LOW"),
    ("r4", "HIGH"),
    ("r5", "LOW")
]

for req_id, priority in requests:
    decision = sq.admit_request(req_id, priority)
    print(req_id, decision)

print("\nState: ", sq.get_state())

sq.on_worker_complete()
sq.on_worker_complete()

print("\nFinal State: ", sq.get_state())