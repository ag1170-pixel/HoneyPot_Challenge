from typing import Dict, Any
from models import HoneypotRequest, SessionState, ScamDetectionResult
from sessions import session_store
from callback import callback_manager

def detect_scam(message: str, history: list) -> ScamDetectionResult:
    """
    Deterministic rule-based scam detection.
    Focuses on urgency, account threats, payment requests, and authority impersonation.
    """
    import re
    
    # Convert to lowercase for case-insensitive matching
    message_lower = message.lower()
    
    # Core scam signal patterns
    urgency_patterns = [
        r'\burgent\b',
        r'\bimmediately\b', 
        r'\bright now\b',
        r'\basap\b',
        r'\btoday only\b',
        r'\blimited time\b',
        r'\bact fast\b',
        r'\bdon\'t delay\b',
        r'\blast chance\b',
        r'\boffer expires\b',
        r'\bending soon\b',
        r'\bquick action\b',
        r'\b24 hours\b',
        r'\b48 hours\b'
    ]
    
    account_threat_patterns = [
        r'\baccount blocked\b',
        r'\baccount suspended\b',
        r'\baccount closed\b',
        r'\baccount frozen\b',
        r'\baccount deactivated\b',
        r'\bsuspend\b',
        r'\bblock\b',
        r'\bdeactivate\b',
        r'\bclose\b',
        r'\bfrozen\b',
        r'\blegal action\b',
        r'\barrest\b',
        r'\bjail\b',
        r'\bprison\b',
        r'\bcourt case\b',
        r'\bcriminal\b',
        r'\bfraud\b',
        r'\billegal\b',
        r'\bviolation\b',
        r'\bseized\b'
    ]
    
    payment_verification_patterns = [
        r'\bpayment\b',
        r'\btransfer\b',
        r'\bsend money\b',
        r'\bdeposit\b',
        r'\bpay\b',
        r'\bcharge\b',
        r'\bfee\b',
        r'\bfine\b',
        r'\bpenalty\b',
        r'\btransaction\b',
        r'\bu?pi\b',
        r'\bupi\b',
        r'\bkyc\b',
        r'\bverify\b',
        r'\bverification\b',
        r'\bconfirm\b',
        r'\bupdate\b',
        r'\bshare\b',
        r'\bprovide\b',
        r'\bgive\b'
    ]
    
    authority_patterns = [
        r'\bbank\b',
        r'\bgovernment\b',
        r'\btax\b',
        r'\bcustoms\b',
        r'\bcourt\b',
        r'\bpolice\b',
        r'\binvestigation\b',
        r'\bofficial\b',
        r'\bdepartment\b',
        r'\brai\b',
        r'\bincome tax\b',
        r'\bgst\b',
        r'\bsebi\b',
        r'\brbi\b',
        r'\breserve bank\b',
        r'\bcyber cell\b',
        r'\bfbi\b',
        r'\binterpol\b',
        r'\bsecurity\b',
        r'\bsbi\b',
        r'\bicici\b',
        r'\bhdfc\b',
        r'\baxis\b',
        r'\bpnb\b',
        r'\bsupport\b'
    ]
    
    # Track detected signals and confidence
    detected_signals = []
    confidence = 0.0
    
    # Check each pattern category
    for pattern in urgency_patterns:
        if re.search(pattern, message_lower):
            detected_signals.append(f"Urgency language: {pattern}")
            confidence += 0.25
    
    for pattern in account_threat_patterns:
        if re.search(pattern, message_lower):
            detected_signals.append(f"Account threat: {pattern}")
            confidence += 0.30
    
    for pattern in payment_verification_patterns:
        if re.search(pattern, message_lower):
            detected_signals.append(f"Payment/verification request: {pattern}")
            confidence += 0.25
    
    for pattern in authority_patterns:
        if re.search(pattern, message_lower):
            detected_signals.append(f"Authority impersonation: {pattern}")
            confidence += 0.20
    
    # Check for suspicious phone number requests
    phone_request_patterns = [
        r'\bcall\s+me\s+on\s+\+?\d{10,15}\b',
        r'\bcall\s+me\s+on\s+\d{10}\b',
        r'\bcall\s+\+?\d{10,15}\b',
        r'\bphone\s+\+?\d{10,15}\b',
        r'\bmobile\s+\+?\d{10,15}\b',
        r'\bcontact\s+\+?\d{10,15}\b',
        r'\+?\d{10,15}\s+for\s+(?:help|support|details|info)'
    ]
    
    for pattern in phone_request_patterns:
        if re.search(pattern, message_lower):
            detected_signals.append(f"Suspicious phone request: {pattern}")
            confidence += 0.25
            break
    
    # Cap confidence at 1.0
    confidence = min(confidence, 1.0)
    
    # Determine if scam is detected
    # Lower threshold for better detection - multiple signals increase confidence
    scam_detected = confidence >= 0.40
    
    return ScamDetectionResult(
        scamDetected=scam_detected,
        confidence=confidence,
        reasons=detected_signals if detected_signals else ["No scam indicators detected"]
    )

def agent_reply(session_state: SessionState) -> str:
    """
    Generate replies as a cautious, cooperative, mildly confused Indian user.
    Asks at most one question per turn.
    """
    import random
    
    # Generic cautious responses
    safe_responses = [
        "I see. Can you please explain this more clearly?",
        "I'm not sure I understand. Could you tell me more about this?",
        "Thank you for the information. What do you need me to do exactly?",
        "I need some time to think about this. What are the next steps?",
        "I'm a bit confused about this process. Can you guide me?",
        "Okay, I understand. How does this work exactly?",
        "I see. What should I do now?",
        "Thank you for explaining. Is there anything else I should know?",
        "I'm not very familiar with these things. Can you help me understand?",
        "Alright. What information do you need from me?"
    ]
    
    # Responses for when personal info is requested
    caution_responses = [
        "I'm not comfortable sharing that information right now. Why do you need it?",
        "I need to be careful with my details. Can you explain why this is necessary?",
        "I'm hesitant to provide that. Is there another way to proceed?",
        "I'd like to understand more before sharing any personal information."
    ]
    
    # Enhanced cautious responses for payment requests
    payment_caution_responses = [
        "I need to think about this carefully. Can you provide more details?",
        "I'm not sure about making payments like this. What are my options?",
        "I need to understand this better before proceeding with any payment.",
        "Can you explain why this payment is necessary? I want to be sure.",
        "I'm hesitant to send money without understanding the process better."
    ]
    
    # Enhanced responses for urgency
    urgency_responses = [
        "I need some time to understand this properly. Can we slow down a bit?",
        "This seems rushed. Can you explain everything step by step?",
        "I prefer to take my time with important decisions. What's the hurry?",
        "Let me understand this first before taking any quick action."
    ]
    
    # Get the last message from conversation history
    last_message = ""
    if session_state.conversation_history:
        last_message = session_state.conversation_history[-1].get("text", "").lower()
    
    # Check if personal information is being requested
    personal_info_keywords = ["account number", "card number", "cvv", "pin", "password", "otp", "aadhaar", "pan"]
    if any(keyword in last_message for keyword in personal_info_keywords):
        return random.choice(caution_responses)
    
    # Check if payment is being requested
    payment_keywords = ["payment", "transfer", "send money", "deposit", "pay", "fee", "charge"]
    if any(keyword in last_message for keyword in payment_keywords):
        return random.choice(payment_caution_responses)
    
    # Check for urgency - be more cautious
    urgency_keywords = ["urgent", "immediately", "right now", "asap", "today only", "hurry", "fast", "quickly", "don't delay", "act now"]
    if any(keyword in last_message for keyword in urgency_keywords):
        return random.choice(urgency_responses)
    
    # Default cautious response
    return random.choice(safe_responses)

def extract_intelligence(text: str, intelligence_store: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only explicitly present intelligence from message text.
    Uses regex for deterministic extraction.
    """
    import re
    
    # Make a copy to avoid modifying the original
    extracted = intelligence_store.copy()
    
    # Initialize categories if not present
    if "upi_ids" not in extracted:
        extracted["upi_ids"] = []
    if "bank_accounts" not in extracted:
        extracted["bank_accounts"] = []
    if "phone_numbers" not in extracted:
        extracted["phone_numbers"] = []
    if "urls" not in extracted:
        extracted["urls"] = []
    if "suspicious_keywords" not in extracted:
        extracted["suspicious_keywords"] = []
    
    # Extract UPI IDs (format: username@bankname)
    upi_pattern = r'\b[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\b'
    upi_matches = re.findall(upi_pattern, text)
    for upi in upi_matches:
        if upi not in extracted["upi_ids"]:
            extracted["upi_ids"].append(upi)
    
    # Extract bank account numbers (10-18 digit sequences)
    account_pattern = r'\b\d{10,18}\b'
    account_matches = re.findall(account_pattern, text)
    for account in account_matches:
        # Avoid extracting phone numbers as account numbers
        if not (len(account) == 10 and account.startswith(('6', '7', '8', '9'))):
            if account not in extracted["bank_accounts"]:
                extracted["bank_accounts"].append(account)
    
    # Extract phone numbers (Indian format - enhanced patterns)
    phone_patterns = [
        r'\b[+]?91[-\s]?[6-9]\d{9}\b',  # +91 format
        r'\b[6-9]\d{9}\b',              # Simple 10-digit
        r'\b0[-\s]?[6-9]\d{9}\b',        # With 0 prefix
        r'\b\d{10}\b',                   # Any 10-digit (catch-all)
        r'\b[+]?\d{11,15}\b'             # International numbers
    ]
    
    for pattern in phone_patterns:
        phone_matches = re.findall(pattern, text)
        for phone in phone_matches:
            # Normalize phone number format
            normalized = re.sub(r'[^0-9+]', '', phone)
            # Avoid duplicates
            if normalized not in extracted["phone_numbers"]:
                extracted["phone_numbers"].append(normalized)
    
    # Extract URLs
    url_pattern = r'\bhttps?://[^\s<>"\']+(?:/[^\s<>"\']*)*\b'
    url_matches = re.findall(url_pattern, text, re.IGNORECASE)
    for url in url_matches:
        if url not in extracted["urls"]:
            extracted["urls"].append(url)
    
    # Extract suspicious keywords
    suspicious_keywords = [
        "urgent", "immediately", "payment", "transfer", "deposit",
        "prize", "winner", "lottery", "bonus", "reward",
        "suspend", "block", "deactivate", "legal action",
        "account number", "card number", "cvv", "pin", "password",
        "otp", "aadhaar", "pan", "tax", "customs", "court",
        "police", "government", "official", "department"
    ]
    
    text_lower = text.lower()
    for keyword in suspicious_keywords:
        if keyword in text_lower and keyword not in extracted["suspicious_keywords"]:
            extracted["suspicious_keywords"].append(keyword)
    
    return extracted

def get_safe_reply() -> str:
    return "Thank you for your message. How can I help you today?"

class HoneypotHandler:
    def __init__(self):
        self.session_store = session_store
        self.callback_manager = callback_manager
    
    def handle_message(self, request: HoneypotRequest) -> Dict[str, Any]:
        session_state = self.session_store.get_session(request.sessionId)
        
        session_state.conversation_history.append({
            "sender": request.message.sender,
            "text": request.message.text,
            "timestamp": request.message.timestamp.isoformat()
        })
        session_state.total_message_count += 1
        
        if not session_state.scam_detected:
            scam_result = detect_scam(request.message.text, session_state.conversation_history)
            if scam_result.scamDetected:
                session_state.scam_detected = True
        
        if session_state.scam_detected:
            previous_intel_count = len(session_state.extracted_intelligence)
            new_intelligence = extract_intelligence(request.message.text, session_state.extracted_intelligence)
            session_state.extracted_intelligence.update(new_intelligence)
            
            if len(session_state.extracted_intelligence) > previous_intel_count:
                session_state.consecutive_no_new_intel = 0
            else:
                session_state.consecutive_no_new_intel += 1
            
            reply = agent_reply(session_state)
        else:
            reply = get_safe_reply()
        
        self.session_store.update_session(request.sessionId, session_state)
        
        if self.session_store.should_stop_session(session_state):
            self.callback_manager.send_final_callback(request.sessionId, session_state)
        
        return {
            "reply": reply,
            "scamDetected": session_state.scam_detected,
            "sessionId": request.sessionId
        }
