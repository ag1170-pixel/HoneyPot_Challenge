#!/usr/bin/env python3
"""
Debug test for the specific message from Swagger UI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handler import detect_scam

def debug_specific_message():
    """Test the specific message that's failing"""
    
    message = "Your bank account will be blocked today. Verify immediately."
    
    print("=" * 80)
    print("DEBUGGING SPECIFIC MESSAGE")
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
    
    # Check urgency patterns
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
    
    print("Urgency patterns:")
    for pattern in urgency_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"  ✓ MATCH: {pattern} -> '{match.group()}'")
    
    # Check account threat patterns
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
    
    print("\nAccount threat patterns:")
    for pattern in account_threat_patterns:
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
        r'\bsecurity\b'
    ]
    
    print("\nAuthority patterns:")
    for pattern in authority_patterns:
        match = re.search(pattern, message_lower)
        if match:
            print(f"  ✓ MATCH: {pattern} -> '{match.group()}'")

if __name__ == "__main__":
    debug_specific_message()
