import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from spotify.config import logger, AWS_S3_BUCKET_NAME, AWS_S3_REGION_NAME

def create_bucket(bucket_name, region_name):
    s3 = boto3.client('s3', region_name=region_name)
    try:
        if region_name == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                'LocationConstraint': region_name})
        logger.info(f"Bucket {bucket_name} created successfully in {region_name}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        logger.info(f"Bucket {bucket_name} already exists and is owned by you")
    except s3.exceptions.BucketAlreadyExists:
        logger.info(f"Bucket {bucket_name} already exists")
    except ClientError as e:
        logger.error(f"Error creating bucket: {e}")

def upload_file_to_s3(file_path, bucket_name, s3_key):
    s3 = boto3.client('s3', region_name=AWS_S3_REGION_NAME)
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        logger.info(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found")
    except NoCredentialsError:
        logger.error("Credentials not available")
    except ClientError as e:
        logger.error(f"Client error: {e}")

def upload_directory_to_s3(directory_path, bucket_name, s3_directory):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.join(s3_directory, file)
            upload_file_to_s3(file_path, bucket_name, s3_key)
