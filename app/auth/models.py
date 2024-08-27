import boto3
from werkzeug.security import generate_password_hash, check_password_hash
from botocore.exceptions import ClientError
from app.extensions import get_dynamodb_resource
from boto3.dynamodb.conditions import Key

dynamodb = get_dynamodb_resource()
user_table = dynamodb.Table('user')

class User:
    def __init__(self, first_name=None, last_name=None, email=None, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def get_user_by_email(cls, email):
        response = user_table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        if response['Items']:
            return cls(**response['Items'][0])
        return None

    def save_to_db(self):
        try:
            user_table.put_item(
                Item={
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'email': self.email,
                    'password': self.password
                },
                ConditionExpression='attribute_not_exists(email)'
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return None
            else:
                raise

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
