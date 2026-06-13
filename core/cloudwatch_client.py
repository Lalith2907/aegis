import boto3

cloudwatch = boto3.client("cloudwatch", region_name="ap-southeast-2")

NAMESPACE = "AEGIS"

def publish_metric (metric_name, value):
    cloudwatch.put_metric_data (
        Namespace=NAMESPACE,
        MetricData=[
            {
                "MetricName": metric_name,
                "Value": value,
                "Unit": "Count"
            }
        ]
    )
