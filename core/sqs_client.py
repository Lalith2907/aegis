import boto3
import os
from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

sqs = boto3.client("sqs", region_name="ap-southeast-2")

def send_to_queue(request_id, priority):
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=request_id,
        MessageAttributes={
            "priority": {
                "StringValue": priority,
                "DataType": "String"
            }
        }
    )
    print(f"[SQS] Request {request_id} sent to SQS")
    return response

def get_queue_depth():
    response = sqs.get_queue_attributes(
        QueueUrl=QUEUE_URL,
        AttributeNames=["ApproximateNumberOfMessages"]
    )
    return int(response["Attributes"]["ApproximateNumberOfMessages"])