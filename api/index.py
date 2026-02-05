import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Import your existing app
from app import app as honeypot_app

# Vercel entry point
async def handler(request):
    """
    Vercel serverless function handler
    """
    try:
        # Get request method and path
        method = request.method
        path = request.url.path
        
        # Get headers
        headers = dict(request.headers)
        
        # Get body for POST requests
        body = None
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = await request.json()
            except:
                body = {}
        
        # Create a mock request for FastAPI
        from fastapi.testclient import TestClient
        client = TestClient(honeypot_app)
        
        # Route the request
        if method == 'GET':
            response = client.get(path, headers=headers)
        elif method == 'POST':
            response = client.post(path, json=body, headers=headers)
        elif method == 'PUT':
            response = client.put(path, json=body, headers=headers)
        elif method == 'DELETE':
            response = client.delete(path, headers=headers)
        else:
            response = client.request(method, path, json=body, headers=headers)
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# Export for Vercel
app = handler
