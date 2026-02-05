from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from models import HoneypotRequest
from auth import validate_api_key
from handler import HoneypotHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Honeypot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

honeypot_handler = HoneypotHandler()

@app.get("/")
async def root():
    return {"message": "Honeypot API is running", "version": "1.0.0"}

@app.post("/honeypot/message")
async def handle_honeypot_message(
    request: HoneypotRequest,
    api_key: str = Depends(validate_api_key)
):
    try:
        result = honeypot_handler.handle_message(request)
        return result
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Vercel serverless handler
def handler(event, context):
    """
    Vercel serverless function handler using ASGI adapter
    """
    try:
        from mangum import Mangum
        asgi_handler = Mangum(app)
        return asgi_handler(event, context)
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': '{"error": "Internal server error"}'
        }

# Export for Vercel
app.handler = handler
