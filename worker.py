import boto3
import os
import time
from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

sqs = boto3.client("sqs", region_name="ap-southeast-2")

print("[WORKER] Worker started...")

while True:
    response = sqs.receive_message (
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
        MessageAttributeNames=["All"]
    )

    messages = response.get("Messages", [])

    if not messages:
        continue

    for message in messages:
        request_id = message["Body"]

        priority = (
            message.get("MessageAttributes", {})
            .get("priority", {})
            .get("StringValue", "LOW")
        )

        print(f"[WORKER] Processing request {request_id} | Priority: {priority}")

        time.sleep(5)

        sqs.delete_message (
            QueueUrl=QUEUE_URL,
            ReceiptHandle=message["ReceiptHandle"]
        )

        print(f"[WORKER] Completed request {request_id}")