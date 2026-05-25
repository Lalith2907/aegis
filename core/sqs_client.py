import boto3

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

sqs = boto3.client("sqs", region_name="ap-southeast-2")

def send_to_queue(request_id, priority):
    response = sqs.send_message (
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
