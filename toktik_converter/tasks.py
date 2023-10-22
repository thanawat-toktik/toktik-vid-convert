import os

import boto3
from botocore.config import Config
from celery import Celery
from dotenv import load_dotenv

from toktik_converter.converter import download_file_from_s3, convert_to_mp4, upload_converted_to_s3


def create_celery_app():
    load_dotenv()
    internal_app = Celery("converter", broker=f"amqp://"
                                              f"{os.environ.get('MQ_USERNAME', 'guest')}"
                                              f":{os.environ.get('MQ_PASSWORD', 'guest')}"
                                              f"@{os.environ.get('MQ_HOSTNAME', 'localhost')}"
                                              f":{os.environ.get('MQ_PORT', '5673')}")
    return internal_app


app = create_celery_app()


@app.task
def do_conversion(object_name):
    load_dotenv()
    client = boto3.client(
        "s3",
        region_name=os.environ.get("S3_REGION"),
        endpoint_url=os.environ.get("S3_RAW_ENDPOINT"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        config=Config(s3={"addressing_style": "virtual"}, signature_version="v4"),
    )
    try:
        downloaded_file = download_file_from_s3(client, object_name)
        converted_file = convert_to_mp4(downloaded_file)
        res = upload_converted_to_s3(client, converted_file)
        return res
    except Exception as e:
        return str(e)
