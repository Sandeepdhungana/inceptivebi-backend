import boto3
import os


class S3Utils:
    def __init__(self, bucket_name) -> None:
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        )

    def generate_presigned_url(self, file_name="", expires_in=180):
        try:
            signed_url = self.s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': self.bucket_name, 'Key': file_name},
                ExpiresIn=expires_in
            )
            return signed_url
        except Exception as e:
            print("Error occurred ", e)

    def get_s3_files(self, file_name):
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            file_content = response['Body'].read()
            return file_content
        except Exception as e:
            print(f"Error retrieving file: {e}")
            return None
