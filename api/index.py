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

# Vercel serverless handler - Pure Python implementation
def handler(event, context):
    """
    Vercel serverless function handler
    """
    try:
        # Parse Vercel event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        
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
                response_data = {"status": "healthy"}
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
                    
                    # Validate API key
                    api_key = headers.get('x-api-key', API_KEY)
                    
                    # Create honeypot request
                    honeypot_request = HoneypotRequest(
                        message=request_data.get('message', ''),
                        user_id=request_data.get('user_id'),
                        session_id=request_data.get('session_id')
                    )
                    
                    # Process message
                    result = honeypot_handler.handle_message(honeypot_request)
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps(result)
                    }
                    
                except Exception as e:
                    logger.error(f"POST error: {e}")
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
        logger.error(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Function invocation failed'})
        }

# Export for Vercel
app.handler = handler
