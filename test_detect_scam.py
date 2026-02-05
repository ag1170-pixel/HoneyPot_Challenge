#!/usr/bin/env python3
"""
Test script for detect_scam() function
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from handler import detect_scam

def test_detect_scam():
    """Test the detect_scam function with various sample messages"""
    
    test_cases = [
        # Clear scam messages
        {
            "message": "URGENT: Your account will be blocked immediately. Verify your account now.",
            "expected": "SCAM"
        },
        {
            "message": "This is RBI Bank. Your account has been suspended. Please call us immediately to verify.",
            "expected": "SCAM"
        },
        {
            "message": "Payment required immediately. Share your UPI details for KYC verification.",
            "expected": "SCAM"
        },
        {
            "message": "LEGAL ACTION: Your account will be closed in 24 hours. Pay the fine now.",
            "expected": "SCAM"
        },
        
        # Borderline cases
        {
            "message": "Please verify your account details for security purposes.",
            "expected": "SCAM"
        },
        {
            "message": "Urgent update required for your bank account.",
            "expected": "SCAM"
        },
        
        # Safe messages
        {
            "message": "Hello, how are you today?",
            "expected": "SAFE"
        },
        {
            "message": "Thank you for your message. I will get back to you soon.",
            "expected": "SAFE"
        },
        {
            "message": "The weather is nice today.",
            "expected": "SAFE"
        },
        {
            "message": "I need help with my homework.",
            "expected": "SAFE"
        }
    ]
    
    print("=" * 80)
    print("TESTING detect_scam() FUNCTION")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        message = test_case["message"]
        expected = test_case["expected"]
        
        result = detect_scam(message, [])
        
        print(f"\nTest Case {i}:")
        print(f"Message: {message}")
        print(f"Expected: {expected}")
        print(f"Result: {'SCAM' if result.scamDetected else 'SAFE'}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"Reasons: {', '.join(result.reasons[:3])}")  # Show first 3 reasons
        print(f"Status: {'✓ PASS' if (result.scamDetected and expected == 'SCAM') or (not result.scamDetected and expected == 'SAFE') else '✗ FAIL'}")
        print("-" * 60)

if __name__ == "__main__":
    test_detect_scam()
