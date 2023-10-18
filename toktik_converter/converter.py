from pathlib import Path
import os

import boto3
from botocore.client import Config
from dotenv import load_dotenv
import ffmpeg


def download_file_from_s3(s3, object_name):
    file_name, file_extension = object_name.split(".")
    temp_folder = Path("/tmp") / file_name
    temp_folder.mkdir(parents=True, exist_ok=True)

    download_target = Path(f"{temp_folder}/{file_name}.{file_extension}")
    s3.download_file(os.environ.get("S3_BUCKET_NAME"), object_name, download_target)
    return download_target


def convert_to_mp4(file_path: Path):
    file_name, file_extension = os.path.splitext(file_path)
    ffmpeg.input(file_path).output(f"{file_name}.mp4", vcodec="libx264").run(quiet=True)

    if file_extension != "mp4":
        os.remove(file_path)

    return Path(f"{file_name}.mp4")


if __name__ == "__main__":
    load_dotenv()
    s3 = boto3.client(
        "s3",
        region_name=os.environ.get("S3_REGION"),
        endpoint_url=os.environ.get("S3_RAW_ENDPOINT"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        config=Config(s3={"addressing_style": "virtual"}, signature_version="v4"),
    )
    downloaded_path = download_file_from_s3(s3, "IMG_6376.MOV")
    converted_path = convert_to_mp4(downloaded_path)
