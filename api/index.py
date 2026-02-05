from fastapi import FastAPI
from fastapi.testclient import TestClient
import json

# Import your existing FastAPI app
from app import app as fastapi_app

# Create test client
client = TestClient(fastapi_app)

# Vercel serverless function handler
def handler(request):
    """
    Main handler for Vercel serverless functions
    """
    try:
        # Extract request data
        method = request.method
        path = request.url.path
        headers = dict(request.headers)
        
        # Get query parameters
        query_params = dict(request.query_params)
        
        # Get body for POST/PUT requests
        body = None
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = request.json()
            except:
                body = {}
        
        # Make request to FastAPI app
        if method == 'GET':
            response = client.get(path, headers=headers, params=query_params)
        elif method == 'POST':
            response = client.post(path, json=body, headers=headers, params=query_params)
        elif method == 'PUT':
            response = client.put(path, json=body, headers=headers, params=query_params)
        elif method == 'DELETE':
            response = client.delete(path, headers=headers, params=query_params)
        else:
            response = client.request(method, path, json=body, headers=headers, params=query_params)
        
        # Return response in Vercel format
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.content.decode('utf-8')
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# Export for Vercel
app = handler
