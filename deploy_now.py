#!/usr/bin/env python3
"""
Quick deployment verification script
Run this after deploying to verify everything works
"""

import requests
import json
from datetime import datetime

# Configuration
DEPLOYED_URL = "https://honey-pot-challenge.onrender.com"
API_KEY = "test-key-12345"

def test_deployed_service():
    """Test the deployed service comprehensively"""
    print("🚀 TESTING DEPLOYED SERVICE")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{DEPLOYED_URL}/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ Health: {response.json()}")
        else:
            print(f"❌ Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health error: {e}")
        return False
    
    # Test 2: Scam Detection
    print("\n2️⃣ Testing Scam Detection...")
    scam_body = {
        "sessionId": "deploy-test-scam",
        "message": {
            "sender": "scammer",
            "text": "URGENT: Your bank account will be blocked. Click here now!",
            "timestamp": datetime.now().isoformat()
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "WhatsApp",
            "language": "English",
            "locale": "IN"
        }
    }
    
    try:
        response = requests.post(
            f"{DEPLOYED_URL}/honeypot/message",
            json=scam_body,
            headers={"x-api-key": API_KEY},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Scam Detection: {result}")
            if result.get("scamDetected") == True:
                print("✅ Scam correctly detected")
            else:
                print("❌ Scam not detected")
                return False
        else:
            print(f"❌ Scam test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Scam test error: {e}")
        return False
    
    # Test 3: Normal Message
    print("\n3️⃣ Testing Normal Message...")
    normal_body = {
        "sessionId": "deploy-test-normal",
        "message": {
            "sender": "user",
            "text": "Hello, how are you today?",
            "timestamp": datetime.now().isoformat()
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "WhatsApp",
            "language": "English",
            "locale": "IN"
        }
    }
    
    try:
        response = requests.post(
            f"{DEPLOYED_URL}/honeypot/message",
            json=normal_body,
            headers={"x-api-key": API_KEY},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Normal Message: {result}")
            if result.get("scamDetected") == False:
                print("✅ Normal message correctly identified")
            else:
                print("❌ Normal message flagged as scam")
                return False
        else:
            print(f"❌ Normal test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Normal test error: {e}")
        return False
    
    # Test 4: Authentication
    print("\n4️⃣ Testing Authentication...")
    try:
        response = requests.post(
            f"{DEPLOYED_URL}/honeypot/message",
            json=scam_body,
            headers={"x-api-key": "wrong-key"},
            timeout=10
        )
        if response.status_code == 403:
            print("✅ Invalid API key correctly rejected")
        else:
            print(f"❌ Should return 403, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Auth test error: {e}")
        return False
    
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Your deployment is READY for hackathon submission!")
    return True

if __name__ == "__main__":
    success = test_deployed_service()
    if not success:
        print("\n❌ DEPLOYMENT FAILED")
        print("Check your Render dashboard for errors")
