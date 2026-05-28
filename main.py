from fastapi import FastAPI, HTTPException
from core.smart_queue import SmartQueue, Decision
import asyncio

app = FastAPI()

sq = SmartQueue(max_workers=2, max_queue_size=3)

@app.get("/api")
async def protected_api(priority: str = "LOW"):
    request_id = str(id(asyncio.current_task()))
    decision = sq.admit_request(request_id, priority)
    
    if decision == Decision.REJECT:
        raise HTTPException(
            status_code=429,
            detail="Request Rejected - System Overloaded"
        )

    if decision == Decision.WAIT:
        return {
            "message": "Request queued in SQS",
            "priority": priority,
            "status": "WAIT"
        }

    try:
        await asyncio.sleep(5)
        return {
            "message": "Request processed successfully",
            "priority": priority,
            "status": "ACCEPT"
        }
    finally:
        sq.on_worker_complete()

@app.get("/metrics")
def get_metrics():
    return sq.get_state()