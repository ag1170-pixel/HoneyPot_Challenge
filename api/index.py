import json

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({"status": "healthy", "message": "Honeypot API is running"})
    }
