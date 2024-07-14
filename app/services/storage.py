import boto3
from botocore.exceptions import ClientError
from flask import current_app
import io

def get_s3_client():
    return boto3.client('s3',
        region_name=current_app.config['SPACES_REGION'],
        endpoint_url=f"https://{current_app.config['SPACES_REGION']}.digitaloceanspaces.com",
        aws_access_key_id=current_app.config['SPACES_KEY'],
        aws_secret_access_key=current_app.config['SPACES_SECRET']
    )

def upload_file_to_spaces(file, filename=None):
    if filename is None:
        filename = file.filename
    
    client = get_s3_client()
    
    try:
        client.upload_fileobj(
            file,
            current_app.config['SPACES_BUCKET'],
            filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type if hasattr(file, 'content_type') else 'application/octet-stream'
            }
        )
    except ClientError as e:
        print(f"Error uploading file: {e}")
        return None

    return f"https://{current_app.config['SPACES_BUCKET']}.{current_app.config['SPACES_REGION']}.digitaloceanspaces.com/{filename}"

def download_file_from_spaces(file_url):
    client = get_s3_client()
    bucket = current_app.config['SPACES_BUCKET']
    key = file_url.split('/')[-1]

    try:
        response = client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return None