import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from pathlib import Path


def download_file_from_s3(object_name: str) -> Path:
    """
    Downloads a file from S3

    Args:
        object_name (str): The key of the object to download

    Returns:
        Path: The path to where the file was downloaded
    """
    load_dotenv()
    s3 = boto3.client(
        "s3",
        region_name=os.environ.get("S3_REGION"),
        endpoint_url=os.environ.get("S3_RAW_ENDPOINT"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        config=Config(s3={"addressing_style": "virtual"}, signature_version="v4"),
    )

    file_name, file_extension = object_name.split(".")
    temp_folder = Path("/tmp") / file_name
    temp_folder.mkdir(parents=True, exist_ok=True)

    download_target = Path(f"{temp_folder}/{file_name}.{file_extension}")
    s3.download_file(os.environ.get("S3_BUCKET_NAME"), object_name, download_target)
    return download_target


if __name__ == "__main__":
    download_file_from_s3("cupfka.mp4")
