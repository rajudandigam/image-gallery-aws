# Image Processor
import boto3
import uuid
import os
from PIL import Image
from io import BytesIO
import datetime

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

UPLOAD_BUCKET = 'pravesh-image-uploads-bucket'
THUMBNAIL_BUCKET = 'pravesh-thumbnails-bucket'
DDB_TABLE = 'image_metadata'

def lambda_handler(event, context):
    # Get uploaded image details
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    # Download the image
    response = s3.get_object(Bucket=bucket, Key=key)
    image = Image.open(BytesIO(response['Body'].read()))

    # Generate Thumbnail
    image.thumbnail((200, 200))

    # Save thumbnail in memory
    thumbnail_buffer = BytesIO()
    image.save(thumbnail_buffer, 'JPEG')
    thumbnail_buffer.seek(0)

    # Upload Thumbnail to S3
    thumbnail_key = f"thumb_{key}"
    s3.put_object(
        Bucket=THUMBNAIL_BUCKET,
        Key=thumbnail_key,
        Body=thumbnail_buffer,
        ContentType='image/jpeg'
    )

    # Store metadata in DynamoDB
    image_id = str(uuid.uuid4())
    original_url = f"https://{UPLOAD_BUCKET}.s3.amazonaws.com/{key}"
    thumbnail_url = f"https://{THUMBNAIL_BUCKET}.s3.amazonaws.com/{thumbnail_key}"
    uploaded_at = datetime.datetime.now().isoformat()

    dynamodb.put_item(
        TableName=DDB_TABLE,
        Item={
            'image_id': {'S': image_id},
            'original_url': {'S': original_url},
            'thumbnail_url': {'S': thumbnail_url},
            'uploaded_at': {'S': uploaded_at}
        }
    )

    return {
        'statusCode': 200,
        'body': f"Thumbnail created: {thumbnail_url}"
    }




# get-Image-Metadata
import boto3
import json

dynamodb = boto3.client('dynamodb')

TABLE_NAME = 'image_metadata'

def lambda_handler(event, context):
    try:
        # Scan the entire table (for simplicity, no pagination)
        response = dynamodb.scan(TableName=TABLE_NAME)

        # Transform DynamoDB items into JSON format
        images = []
        for item in response['Items']:
            images.append({
                'image_id': item['image_id']['S'],
                'original_url': item['original_url']['S'],
                'thumbnail_url': item['thumbnail_url']['S'],
                'uploaded_at': item['uploaded_at']['S']
            })

        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json"
            },
            'body': json.dumps(images)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
