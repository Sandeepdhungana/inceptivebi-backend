import boto3
import os


lex_client = boto3.client('lexv2-runtime',region_name='us-east-1')


def get_dynamodb_resource():
    return boto3.resource('dynamodb', region_name='us-east-1')
