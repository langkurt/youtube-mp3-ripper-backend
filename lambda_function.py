import json

import boto3

from youtube_rip import download_and_convert

s3_client = boto3.client('s3')


def download_mp3(youtube_url):
    mp3_file_name = download_and_convert(youtube_url)
    print(f"In download_mp3(): got the mp3 file name: '{mp3_file_name}'")
    return mp3_file_name


def lambda_handler(event, context):
    print(f"Entering Lambda Handler. Event is: {event}")

    youtube_url = event['youtube_url']
    bucket_name = "reaped"

    # Business Logic
    file_name = download_mp3(youtube_url)
    file_path = f'/tmp/{file_name}'

    # Upload file to S3
    print(f"Uploading {file_path} to s3 bucket {bucket_name}")
    s3_client.upload_file(file_path, bucket_name, file_name)

    # Get presigned url for uploaded file to grant time-limited permission to download the file.
    params = {'Bucket': bucket_name, 'Key': file_name}
    presigned_url = s3_client.generate_presigned_url('get_object', Params=params, ExpiresIn=300)  # expire in 5 min
    print(f"Presigned URL for uploaded file: {presigned_url}")

    return {
        'statusCode': 200,
        'body': presigned_url
    }
