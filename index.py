from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI()

class Message(BaseModel):
    sender: str
    text: str
    timestamp: datetime

class Metadata(BaseModel):
    channel: str
    language: str
    locale: str

class HoneypotRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Dict[str, Any]]
    metadata: Metadata

@app.get("/")
async def root():
    return {"status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/honeypot/message")
async def handle_message(request: HoneypotRequest):
    is_scam = "bank" in request.message.text.lower()
    
    return {
        "sessionId": request.sessionId,
        "scamDetected": is_scam,
        "confidence": 0.8 if is_scam else 0.2,
        "reasons": ["Financial scam detected"] if is_scam else ["No scam indicators"],
        "agentReply": "Please verify with your bank directly." if is_scam else "Thank you for your message."
    }
