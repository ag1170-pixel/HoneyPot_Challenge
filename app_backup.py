from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import requests
import json

# Import correct models
from models import HoneypotRequest, Message, Metadata, GUVICallbackPayload

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import correct models - using models.py

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

# Proper API key validation
def validate_api_key(api_key: Optional[str] = Header(None, alias="x-api-key")) -> str:
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

# Simple honeypot handler
class SimpleHoneypotHandler:
    def __init__(self):
        self.callback_url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    def handle_message(self, request: HoneypotRequest):
        try:
            # Simple scam detection logic (replace with actual implementation)
            is_scam = "bank" in request.message.text.lower() or "account" in request.message.text.lower()
            confidence = 0.8 if is_scam else 0.2
            
            # Create callback payload matching GUVI format
            callback_payload = GUVICallbackPayload(
                sessionId=request.sessionId,
                scamDetected=is_scam,
                totalMessagesExchanged=len(request.conversationHistory) + 1,
                extractedIntelligence={
                    "bankAccounts": [],
                    "upiIds": [],
                    "phishingLinks": [],
                    "phoneNumbers": [],
                    "suspiciousKeywords": ["bank", "account"] if is_scam else []
                },
                agentNotes=f"Message analyzed: {request.message.text[:100]}..."
            )
            
            # Send callback to GUVI
            try:
                requests.post(self.callback_url, json=callback_payload.dict(), timeout=5)
            except:
                logger.warning("Callback failed")
            
            # Return response in expected format
            return {
                "sessionId": request.sessionId,
                "scamDetected": is_scam,
                "confidence": confidence,
                "reasons": ["Financial scam detected"] if is_scam else ["No scam indicators"],
                "agentReply": "Please verify with your bank directly." if is_scam else "Thank you for your message."
            }
            
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
    api_key: str = Depends(validate_api_key)
):
    try:
        result = honeypot_handler.handle_message(request)
        return result
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Pure FastAPI - no serverless code
