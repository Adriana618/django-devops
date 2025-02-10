import boto3
from django.conf import settings


def upload_file_to_s3(file_obj, file_name):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    s3_client.upload_fileobj(
        file_obj,
        settings.AWS_S3_BUCKET,
        file_name,
        ExtraArgs={"ServerSideEncryption": "AES256"},
    )
    return file_name
