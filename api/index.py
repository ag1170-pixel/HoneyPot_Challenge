import json

def handler(request):
    """
    Vercel serverless function handler - Simplified for reliability
    """
    try:
        # Basic response for health check
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"status": "healthy", "message": "Honeypot API is running"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": f"Internal server error: {str(e)}"})
        }
