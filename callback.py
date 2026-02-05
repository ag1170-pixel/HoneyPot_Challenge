import requests
import logging
from typing import Dict, Any
from models import SessionState, GUVICallbackPayload
from config import config

logger = logging.getLogger(__name__)

class CallbackManager:
    def __init__(self):
        self.sent_callbacks: set = set()
    
    def send_final_callback(self, session_id: str, session_state: SessionState) -> bool:
        if session_id in self.sent_callbacks:
            logger.warning(f"Callback already sent for session {session_id}")
            return False
        
        payload = GUVICallbackPayload(
            sessionId=session_id,
            scamDetected=session_state.scam_detected,
            totalMessagesExchanged=session_state.total_message_count,
            extractedIntelligence=session_state.extracted_intelligence,
            agentNotes="Session completed"
        )
        
        try:
            response = requests.post(
                config.GUVI_CALLBACK_URL,
                json=payload.dict(),
                timeout=10
            )
            response.raise_for_status()
            self.sent_callbacks.add(session_id)
            logger.info(f"Callback sent successfully for session {session_id}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send callback for session {session_id}: {e}")
            return False

callback_manager = CallbackManager()
