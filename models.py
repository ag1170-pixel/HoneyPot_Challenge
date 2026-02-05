from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

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

class ScamDetectionResult(BaseModel):
    scamDetected: bool
    confidence: float
    reasons: List[str]

class SessionState(BaseModel):
    conversation_history: List[Dict[str, Any]]
    scam_detected: bool
    total_message_count: int
    extracted_intelligence: Dict[str, Any]
    consecutive_no_new_intel: int

class GUVICallbackPayload(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: Dict[str, Any]
    agentNotes: str
