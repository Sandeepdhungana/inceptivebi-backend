import os
import boto3

# Fetch AWS credentials from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')

# Create the Lex client using credentials from environment variables
lex_client = boto3.client(
    'lexv2-runtime',
    region_name='us-east-1',
)

# Function to get DynamoDB resource using credentials from environment variables
def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        region_name='us-east-1',
    )
# # Create the Lex client using credentials from environment variables
# lex_client = boto3.client(
#     'lexv2-runtime',
#     region_name='us-east-1',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key
# )

# # Function to get DynamoDB resource using credentials from environment variables
# def get_dynamodb_resource():
#     return boto3.resource(
#         'dynamodb',
#         region_name='us-east-1',
#         aws_access_key_id=aws_access_key_id,
#         aws_secret_access_key=aws_secret_access_key
#     )
