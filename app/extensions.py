import boto3
import os


lex_client = boto3.client('lexv2-runtime')


def get_dynamodb_resource():
    return boto3.resource('dynamodb')
