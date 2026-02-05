#!/usr/bin/env python3
"""
Test the exact API flow to identify why scamDetected is false
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handler import HoneypotHandler
from models import HoneypotRequest, Message, Metadata
from datetime import datetime

def test_api_flow():
    """Test the exact API flow"""
    
    print("=" * 80)
    print("TESTING API FLOW")
    print("=" * 80)
    
    # Create handler
    handler = HoneypotHandler()
    
    # Create request like the Swagger UI
    message_text = "Your bank account will be blocked today. Verify immediately."
    session_id = "test-003"
    
    request = HoneypotRequest(
        sessionId=session_id,
        message=Message(
            sender="scammer",
            text=message_text,
            timestamp=datetime.now()
        ),
        conversationHistory=[],
        metadata=Metadata(
            channel="web",
            language="en",
            locale="IN"
        )
    )
    
    print(f"Input message: {message_text}")
    print(f"Session ID: {session_id}")
    print()
    
    # Get initial session state
    initial_session = handler.session_store.get_session(session_id)
    print(f"Initial session scam_detected: {initial_session.scam_detected}")
    
    # Handle the message
    result = handler.handle_message(request)
    
    print(f"Result scamDetected: {result['scamDetected']}")
    print(f"Result reply: {result['reply']}")
    print()
    
    # Get final session state
    final_session = handler.session_store.get_session(session_id)
    print(f"Final session scam_detected: {final_session.scam_detected}")
    
    # Test detect_scam directly
    from handler import detect_scam
    direct_result = detect_scam(message_text, [])
    print(f"\nDirect detect_scam result:")
    print(f"  scamDetected: {direct_result.scamDetected}")
    print(f"  confidence: {direct_result.confidence}")
    print(f"  reasons: {direct_result.reasons}")

if __name__ == "__main__":
    test_api_flow()
