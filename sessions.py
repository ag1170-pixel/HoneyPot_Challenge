from typing import Dict
from models import SessionState

class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}
    
    def get_session(self, session_id: str) -> SessionState:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(
                conversation_history=[],
                scam_detected=False,
                total_message_count=0,
                extracted_intelligence={},
                consecutive_no_new_intel=0
            )
        return self.sessions[session_id]
    
    def update_session(self, session_id: str, session_state: SessionState) -> None:
        self.sessions[session_id] = session_state
    
    def should_stop_session(self, session_state: SessionState) -> bool:
        return (
            session_state.total_message_count >= 15 or
            session_state.consecutive_no_new_intel >= 3
        )

session_store = SessionStore()
