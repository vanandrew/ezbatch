from boto3 import client

BATCH_CLIENT = client("batch")
STS_CLIENT = client("sts")
IAM_CLIENT = client("iam")
