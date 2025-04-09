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
