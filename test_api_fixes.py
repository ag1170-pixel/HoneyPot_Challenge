#!/usr/bin/env python3
"""
Test script to verify all API fixes are working correctly.
Tests the updated FastAPI application with proper schema and authentication.
"""

import json
import requests
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
API_KEY = "test-key-12345"

def test_health_endpoint():
    """Test the health endpoint"""
    print("=== Testing Health Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
        return True
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}")
        return False

def test_authentication():
    """Test API key authentication"""
    print("\n=== Testing Authentication ===")
    
    # Test with correct API key
    headers = {"x-api-key": API_KEY}
    body = {
        "sessionId": "test-auth",
        "message": {
            "sender": "scammer",
            "text": "Test message",
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
        response = requests.post(f"{BASE_URL}/honeypot/message", 
                               json=body, headers=headers)
        print(f"✓ Valid API key: {response.status_code}")
    except Exception as e:
        print(f"✗ Valid API key failed: {e}")
        return False
    
    # Test with wrong API key
    headers_wrong = {"x-api-key": "wrong-key"}
    try:
        response = requests.post(f"{BASE_URL}/honeypot/message", 
                               json=body, headers=headers_wrong)
        if response.status_code == 403:
            print("✓ Invalid API key correctly rejected (403)")
        else:
            print(f"✗ Invalid API key should return 403, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Invalid API key test failed: {e}")
        return False
    
    # Test without API key
    try:
        response = requests.post(f"{BASE_URL}/honeypot/message", json=body)
        if response.status_code == 401:
            print("✓ Missing API key correctly rejected (401)")
        else:
            print(f"✗ Missing API key should return 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Missing API key test failed: {e}")
        return False
    
    return True

def test_request_schema():
    """Test the correct request schema"""
    print("\n=== Testing Request Schema ===")
    
    headers = {"x-api-key": API_KEY}
    body = {
        "sessionId": "test-schema",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately.",
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
        response = requests.post(f"{BASE_URL}/honeypot/message", 
                               json=body, headers=headers)
        print(f"✓ Schema validation: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"  Response keys: {list(result.keys())}")
            
            # Check expected response fields
            expected_fields = ["sessionId", "scamDetected", "confidence", "reasons", "agentReply"]
            for field in expected_fields:
                if field in result:
                    print(f"  ✓ {field}: {result[field]}")
                else:
                    print(f"  ✗ Missing field: {field}")
                    return False
            
            return True
        else:
            print(f"✗ Schema test failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False

def test_scam_detection():
    """Test scam detection logic"""
    print("\n=== Testing Scam Detection ===")
    
    headers = {"x-api-key": API_KEY}
    
    # Test scam message
    scam_body = {
        "sessionId": "test-scam",
        "message": {
            "sender": "scammer",
            "text": "URGENT: Your bank account will be blocked. Click here now!",
            "timestamp": datetime.now().isoformat()
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/honeypot/message", 
                               json=scam_body, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("scamDetected") == True:
                print("✓ Scam message correctly detected")
                print(f"  Confidence: {result.get('confidence')}")
            else:
                print("✗ Scam message not detected")
                return False
        else:
            print(f"✗ Scam test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Scam test failed: {e}")
        return False
    
    # Test normal message
    normal_body = {
        "sessionId": "test-normal",
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
        response = requests.post(f"{BASE_URL}/honeypot/message", 
                               json=normal_body, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("scamDetected") == False:
                print("✓ Normal message correctly identified as not scam")
                print(f"  Confidence: {result.get('confidence')}")
            else:
                print("✗ Normal message incorrectly flagged as scam")
                return False
        else:
            print(f"✗ Normal message test failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Normal message test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Testing Fixed FastAPI Honeypot API")
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_authentication,
        test_request_schema,
        test_scam_detection
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! API is ready for deployment.")
    else:
        print("❌ Some tests failed. Please fix the issues.")
