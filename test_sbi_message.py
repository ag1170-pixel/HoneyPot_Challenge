#!/usr/bin/env python3
"""
Test the SBI support message that's failing detection
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handler import detect_scam

def test_sbi_message():
    """Test the SBI support message"""
    
    message = "This is SBI support. Call me on 9876543210 to complete verification."
    
    print("=" * 80)
    print("TESTING SBI SUPPORT MESSAGE")
    print("=" * 80)
    print(f"Message: {message}")
    print(f"Message lowercase: {message.lower()}")
    print()
    
    result = detect_scam(message, [])
    
    print(f"Scam Detected: {result.scamDetected}")
    print(f"Confidence: {result.confidence}")
    print(f"Reasons: {result.reasons}")
    print()
    
    # Manual pattern checking
    import re
    message_lower = message.lower()
    
    print("MANUAL PATTERN CHECKING:")
    print("-" * 40)
    
    # Check authority patterns
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
        r'\bsbi\b'  # Add SBI specifically
    ]
    
    print("Authority patterns:")
    for pattern in authority_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"  ✓ MATCH: {pattern} -> '{match.group()}'")
    
    # Check payment/verification patterns
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
    
    print("\nPayment/verification patterns:")
    for pattern in payment_verification_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"  ✓ MATCH: {pattern} -> '{match.group()}'")
    
    # Check phone request patterns
    phone_request_patterns = [
        r'\bcall\s+\+?\d{10,15}\b',
        r'\bphone\s+\+?\d{10,15}\b',
        r'\bmobile\s+\+?\d{10,15}\b',
        r'\bcontact\s+\+?\d{10,15}\b',
        r'\+?\d{10,15}\s+for\s+(?:help|support|details|info)',
        r'\bcall\s+me\s+on\s+\+?\d{10,15}\b',
        r'\bcall\s+me\s+on\s+\d{10}\b'
    ]
    
    print("\nPhone request patterns:")
    for pattern in phone_request_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"  ✓ MATCH: {pattern} -> '{match.group()}'")

if __name__ == "__main__":
    test_sbi_message()
