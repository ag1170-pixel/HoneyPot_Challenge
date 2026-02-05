import json

def handler(event, context):
    """
    Vercel serverless function handler - Correct signature
    """
    try:
        # Parse Vercel event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # Handle favicon requests
        if path == '/favicon.ico' or path == '/favicon.png':
            return {
                'statusCode': 204,
                'headers': {},
                'body': ''
            }
        
        # Route handling
        if http_method == 'GET':
            if path == '/' or path == '/health':
                response_data = {"status": "healthy", "message": "Honeypot API is running"}
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(response_data)
                }
            elif path == '/honeypot/message':
                response_data = {"message": "Honeypot API - POST to this endpoint"}
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(response_data)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({"error": "Not found"})
                }
        
        elif http_method == 'POST':
            if path == '/honeypot/message':
                try:
                    # Parse request body
                    body = event.get('body', '{}')
                    if body:
                        request_data = json.loads(body)
                    else:
                        request_data = {}
                    
                    # Validate API key (accept any for now)
                    api_key = event.get('headers', {}).get('x-api-key', 'test-key-12345')
                    
                    # Simple honeypot response
                    response_data = {
                        "status": "processed",
                        "message": request_data.get('message', ''),
                        "is_scam": False,
                        "confidence": 0.5
                    }
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps(response_data)
                    }
                    
                except Exception as e:
                    return {
                        'statusCode': 500,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({"error": "Internal server error"})
                    }
        
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "Method not allowed"})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Function invocation failed: {str(e)}'})
        }
