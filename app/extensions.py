import boto3
import os


import os
import boto3

aws_access_key_id 

lex_client = boto3.client(
    'lexv2-runtime',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='your-region'  # Replace with your AWS region, e.g., 'us-west-2'
)



def get_dynamodb_resource():
    return boto3.resource('dynamodb')
