#!/usr/bin/env python3
"""
Quick test script to test the running honeypot API with sample requests.
"""

import requests
import json
from datetime import datetime

def test_api_request(message_text, session_id="test-session"):
    """Send a test request to the honeypot API."""
    
    url = "http://127.0.0.1:8000/honeypot/message"
    
    request_data = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": message_text,
            "timestamp": datetime.now().isoformat()
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "whatsapp",
            "language": "en",
            "locale": "IN"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "test-key-12345"
    }
    
    try:
        response = requests.post(
            url,
            json=request_data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS")
            print(f"Message: {message_text}")
            print(f"Scam Detected: {result.get('scamDetected', False)}")
            print(f"Agent Reply: {result.get('reply', 'No reply')}")
            print(f"Session ID: {result.get('sessionId', 'N/A')}")
            print("-" * 60)
            return result
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            print("-" * 60)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("-" * 60)
        return None

def main():
    """Test various scam scenarios."""
    
    print("🍯 TESTING HONEYPOT API 🍯")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        {
            "name": "Bank Account Suspension",
            "message": "URGENT: Your bank account will be SUSPENDED! Call +919876543210 immediately!"
        },
        {
            "name": "Lottery Winner",
            "message": "CONGRATULATIONS! You won $1,000,000! Send $500 to winner@bank to claim prize"
        },
        {
            "name": "Income Tax Scam",
            "message": "This is Income Tax Department. Pay ₹50,000 immediately or face legal action."
        },
        {
            "name": "Safe Message",
            "message": "Hello, how are you doing today?"
        },
        {
            "name": "Romance Emergency",
            "message": "My love, I need money urgently for hospital bills. Please send to help@bank"
        },
        {
            "name": "Job Scam",
            "message": "WORK FROM HOME! Earn ₹50,000/month. Pay ₹1,000 registration fee to start."
        }
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\n🧪 Testing: {test['name']}")
        result = test_api_request(test['message'], f"session-{test['name'].replace(' ', '_')}")
        results.append((test['name'], result))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    scams_detected = 0
    total_tests = len(results)
    
    for name, result in results:
        if result and result.get('scamDetected', False):
            scams_detected += 1
            status = "🚨 SCAM DETECTED"
        elif result:
            status = "✅ SAFE"
        else:
            status = "❌ ERROR"
        
        print(f"{name}: {status}")
    
    print(f"\nScams Detected: {scams_detected}/{total_tests}")
    print(f"Detection Rate: {(scams_detected/total_tests)*100:.1f}%")
    
    print("\n🎯 Your honeypot is working! Visit http://127.0.0.1:8000/docs for more testing")

if __name__ == "__main__":
    main()
