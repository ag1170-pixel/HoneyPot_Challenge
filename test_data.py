#!/usr/bin/env python3
"""
Comprehensive test data for honeypot scam detection.
Contains various scam scenarios and test cases.
"""

import json
from datetime import datetime, timedelta

# Test data for different scam scenarios
TEST_SCENARIOS = {
    "banking_scams": [
        {
            "name": "Account Suspension Scam",
            "message": "URGENT: Your bank account has been SUSPENDED! Call +919876543210 immediately to reactivate. This is your last chance!",
            "expected_scam": True,
            "expected_confidence": 0.8,
            "expected_intel": ["+919876543210"]
        },
        {
            "name": "KYC Verification Scam", 
            "message": "Dear Customer, your KYC verification is incomplete. Update your account details immediately: http://bit.ly/verify-now",
            "expected_scam": True,
            "expected_confidence": 0.7,
            "expected_intel": ["http://bit.ly/verify-now"]
        },
        {
            "name": "Fraud Detection Scam",
            "message": "We detected suspicious activity on your account. Verify your card number and PIN to secure your account.",
            "expected_scam": True,
            "expected_confidence": 0.75,
            "expected_intel": []
        }
    ],
    
    "lottery_prize_scams": [
        {
            "name": "Lottery Winner Scam",
            "message": "CONGRATULATIONS!!! You have won $1,000,000 in our lucky draw! Claim your prize by sending $500 processing fee to winner@bank",
            "expected_scam": True,
            "expected_confidence": 0.85,
            "expected_intel": ["winner@bank"]
        },
        {
            "name": "Amazon Prize Scam",
            "message": "Amazon Lucky Winner! You won an iPhone 15. Pay ₹299 for delivery. Send to amazon.prize@upi",
            "expected_scam": True,
            "expected_confidence": 0.8,
            "expected_intel": ["amazon.prize@upi"]
        }
    ],
    
    "government_authority_scams": [
        {
            "name": "Income Tax Scam",
            "message": "This is Income Tax Department. You have tax dues of ₹50,000. Pay immediately or face legal action. Call 011-23456789",
            "expected_scam": True,
            "expected_confidence": 0.9,
            "expected_intel": ["01123456789"]
        },
        {
            "name": "Customs Seizure Scam",
            "message": "Your package is seized by customs. Pay fine of ₹10,000 to release. Account number: 1234567890123456",
            "expected_scam": True,
            "expected_confidence": 0.85,
            "expected_intel": ["1234567890123456"]
        },
        {
            "name": "Cyber Cell Scam",
            "message": "Cyber Cell Police: Your Aadhaar card is used in illegal activities. Verify your details immediately or arrest warrant will be issued.",
            "expected_scam": True,
            "expected_confidence": 0.9,
            "expected_intel": []
        }
    ],
    
    "romance_scams": [
        {
            "name": "Romance Emergency Scam",
            "message": "My love, I need your help urgently. My mother is in hospital and I need money for treatment. Please send to love.forever@bank",
            "expected_scam": True,
            "expected_confidence": 0.6,
            "expected_intel": ["love.forever@bank"]
        },
        {
            "name": "Dating Investment Scam",
            "message": "Honey, I found a great investment opportunity. Let's build our future together. Send money to crypto.love@upi and I'll double it!",
            "expected_scam": True,
            "expected_confidence": 0.7,
            "expected_intel": ["crypto.love@upi"]
        }
    ],
    
    "investment_scams": [
        {
            "name": "Crypto Investment Scam",
            "message": "GUARANTEED 200% returns on Bitcoin investment! Risk-free opportunity. Invest ₹10,000 and become millionaire in 30 days!",
            "expected_scam": True,
            "expected_confidence": 0.8,
            "expected_intel": []
        },
        {
            "name": "Stock Trading Scam",
            "message": "Exclusive stock tips! Our members doubled their money last month. Join now for ₹50,000 membership fee. Limited slots available!",
            "expected_scam": True,
            "expected_confidence": 0.75,
            "expected_intel": []
        }
    ],
    
    "job_scams": [
        {
            "name": "Work From Home Scam",
            "message": "WORK FROM HOME! Earn ₹50,000 per month doing simple data entry. Pay ₹1,000 registration fee to start. Immediate hiring!",
            "expected_scam": True,
            "expected_confidence": 0.7,
            "expected_intel": []
        },
        {
            "name": "Fake Interview Scam",
            "message": "You are selected for interview at Google! Pay ₹2,000 for background verification. Call +918877665544 for interview schedule.",
            "expected_scam": True,
            "expected_confidence": 0.8,
            "expected_intel": ["+918877665544"]
        }
    ],
    
    "safe_messages": [
        {
            "name": "Normal Greeting",
            "message": "Hello, how are you doing today?",
            "expected_scam": False,
            "expected_confidence": 0.0,
            "expected_intel": []
        },
        {
            "name": "Business Inquiry",
            "message": "Hi, I'm interested in your services. Can you please provide more information about your pricing?",
            "expected_scam": False,
            "expected_confidence": 0.0,
            "expected_intel": []
        },
        {
            "name": "Personal Message",
            "message": "Hey, are we still meeting for lunch tomorrow at 2 PM?",
            "expected_scam": False,
            "expected_confidence": 0.0,
            "expected_intel": []
        }
    ]
}

def generate_test_request(session_id: str, message_text: str, conversation_history: list = None):
    """Generate a test request in the expected API format."""
    if conversation_history is None:
        conversation_history = []
    
    return {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": message_text,
            "timestamp": datetime.now().isoformat()
        },
        "conversationHistory": conversation_history,
        "metadata": {
            "channel": "whatsapp",
            "language": "en",
            "locale": "IN"
        }
    }

def generate_conversation_test():
    """Generate a multi-message conversation test."""
    base_time = datetime.now()
    
    conversation = [
        {
            "name": "Conversation Step 1",
            "message": "Congratulations! You have won a prize in our lucky draw!",
            "expected_scam": True,
            "expected_confidence": 0.6
        },
        {
            "name": "Conversation Step 2", 
            "message": "To claim your prize, you need to pay a small processing fee of ₹500.",
            "expected_scam": True,
            "expected_confidence": 0.8
        },
        {
            "name": "Conversation Step 3",
            "message": "Send the payment immediately to winner@bank or you will lose your prize forever!",
            "expected_scam": True,
            "expected_confidence": 0.9
        }
    ]
    
    return conversation

# Edge cases and boundary tests
EDGE_CASES = [
    {
        "name": "Mixed Case Scam",
        "message": "UrGeNt: YoUr aCcOuNt WiLl Be SuSpEnDeD!!!",
        "expected_scam": True,
        "expected_confidence": 0.5
    },
    {
        "name": "Minimal Scam Indicators",
        "message": "Please update your details soon.",
        "expected_scam": False,
        "expected_confidence": 0.1
    },
    {
        "name": "Multiple Phone Numbers",
        "message": "Call +919876543210 or 01123456789 for immediate assistance!",
        "expected_scam": True,
        "expected_confidence": 0.3,
        "expected_intel": ["+919876543210", "01123456789"]
    },
    {
        "name": "Multiple URLs",
        "message": "Click http://bit.ly/scam1 or https://tinyurl.com/fake2 for details!",
        "expected_scam": True,
        "expected_confidence": 0.4,
        "expected_intel": ["http://bit.ly/scam1", "https://tinyurl.com/fake2"]
    }
]

if __name__ == "__main__":
    # Print sample test cases
    print("=== SAMPLE TEST CASES ===")
    
    # Example of how to use the test data
    for category, tests in TEST_SCENARIOS.items():
        print(f"\n--- {category.upper()} ---")
        for test in tests[:2]:  # Show first 2 tests from each category
            print(f"Test: {test['name']}")
            print(f"Message: {test['message']}")
            print(f"Expected Scam: {test['expected_scam']}")
            print(f"Expected Confidence: {test['expected_confidence']}")
            print("---")
    
    print(f"\nTotal test scenarios: {sum(len(tests) for tests in TEST_SCENARIOS.values())}")
    print(f"Edge cases: {len(EDGE_CASES)}")
