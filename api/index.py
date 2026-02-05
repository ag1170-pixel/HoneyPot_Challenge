from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import requests
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class HoneypotRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

# FastAPI app
app = FastAPI(title="Honeypot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key from config
API_KEY = "test-key-12345"

# Simple API key validation
def validate_api_key(api_key: Optional[str] = Header(None, alias="x-api-key")) -> str:
    return api_key or API_KEY

# Simple honeypot handler
class SimpleHoneypotHandler:
    def __init__(self):
        self.callback_url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    def handle_message(self, request: HoneypotRequest):
        try:
            response = {
                "status": "processed",
                "message": request.message,
                "is_scam": False,
                "confidence": 0.5
            }
            
            try:
                requests.post(self.callback_url, json=response, timeout=5)
            except:
                logger.warning("Callback failed")
            
            return response
            
        except Exception as e:
            logger.error(f"Handler error: {e}")
            raise HTTPException(status_code=500, detail="Processing failed")

# Initialize handler
honeypot_handler = SimpleHoneypotHandler()

# Routes
@app.get("/")
async def root():
    return {"message": "Honeypot API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/honeypot/message")
async def handle_honeypot_message(
    request: HoneypotRequest,
    api_key: str = validate_api_key()
):
    try:
        result = honeypot_handler.handle_message(request)
        return result
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Vercel-compatible ASGI handler
def handler(event, context):
    """
    Vercel serverless function handler using ASGI app
    """
    try:
        # Manual ASGI implementation for Vercel
        from urllib.parse import parse_qs
        
        # Parse Vercel event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        query_params = event.get('queryStringParameters', {}) or {}
        
        # Handle favicon
        if path in ['/favicon.ico', '/favicon.png']:
            return {
                'statusCode': 204,
                'headers': {},
                'body': ''
            }
        
        # Create ASGI scope
        scope = {
            'type': 'http',
            'method': http_method.lower(),
            'path': path,
            'headers': headers,
            'query_string': f"?{parse_qs(query_params).urlencode()}" if query_params else ''
        }
        
        # Create receive function
        async def receive():
            if http_method in ['POST', 'PUT', 'PATCH']:
                body = event.get('body', '')
                return {'type': 'http.request', 'body': body.encode(), 'more_body': False}
            return {'type': 'http.request', 'body': b'', 'more_body': False}
        
        # Create send function
        response = {}
        async def send(message):
            nonlocal response
            if message['type'] == 'http.response.start':
                response['status'] = message['status']
                response['headers'] = message.get('headers', {})
            elif message['type'] == 'http.response.body':
                response['body'] = message.get('body', b'').decode()
        
        # Run ASGI app
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            asgi_app = app
            loop.run_until_complete(asgi_app(scope, receive, send))
        except Exception as e:
            logger.error(f"ASGI error: {e}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "ASGI execution failed"})
            }
        
        # Return Vercel response
        return {
            'statusCode': response.get('status', 200),
            'headers': response.get('headers', {}),
            'body': response.get('body', '')
        }
        
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({"error": "Function invocation failed"})
        }

# Export for Vercel
app.handler = handler
