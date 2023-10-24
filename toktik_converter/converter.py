from pathlib import Path
import shutil
import os

import boto3
from botocore.client import Config
from dotenv import load_dotenv
from ffmpeg import FFmpeg


def download_file_from_s3(client, object_name):
    file_name, file_extension = object_name.split(".")
    temp_folder = Path("/tmp") / file_name
    temp_folder.mkdir(parents=True, exist_ok=True)

    download_target = temp_folder / Path(f"{file_name}.{file_extension}")
    client.download_file(
        os.environ.get("S3_RAW_BUCKET_NAME"), object_name, download_target
    )
    return download_target


def convert_to_mp4(file_path: Path):
    file_name, file_extension = os.path.splitext(file_path)
    if file_extension == ".mp4":
        return file_path

    ffmpeg = (FFmpeg().option("y").input(file_path).output(f"{file_name}.mp4", {"codec:v": "libx264"}))
    ffmpeg.execute()
    return Path(f"/tmp/{file_name}/{file_name}.mp4")


def upload_converted_to_s3(client, file_path: Path):
    client.upload_file(
        file_path,
        os.environ.get("S3_CONVERTED_BUCKET_NAME"),
        file_path.name,
        ExtraArgs={"ContentType": "video/mp4", "ACL": "public-read"},
    )
    temp_folder = file_path.parent
    shutil.rmtree(temp_folder)
    return True


if __name__ == "__main__":
    load_dotenv()
    s3_client = boto3.client(
        "s3",
        region_name=os.environ.get("S3_REGION"),
        endpoint_url=os.environ.get("S3_RAW_ENDPOINT"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("S3_SECRET_ACCESS_KEY"),
        config=Config(s3={"addressing_style": "virtual"}, signature_version="v4"),
    )

    downloaded_path = download_file_from_s3(s3_client, "68cf7a01-f70a-437a-8ae8-9bbb103e89f3.mp4")
    converted_path = convert_to_mp4(downloaded_path)
    # print("convert done")
    # upload_converted_to_s3(s3_client, converted_path)
    # print("upload done")
