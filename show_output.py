#!/usr/bin/env python3
"""
Simple test to show exactly where the output appears
"""

import requests
import json

def test_honeypot_and_show_output():
    """Test the honeypot and show exactly where to look for results"""
    
    print("🍯 TESTING HONEYPOT - WHERE TO SEE OUTPUT 🍯")
    print("=" * 60)
    
    # Test data
    test_data = {
        "sessionId": "demo-session",
        "message": {
            "sender": "scammer",
            "text": "URGENT: Your bank account will be SUSPENDED! Call +919876543210 immediately!",
            "timestamp": "2025-01-01T10:00:00Z"
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
    
    print("📤 SENDING REQUEST...")
    print(f"Message: {test_data['message']['text']}")
    print("-" * 60)
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/honeypot/message",
            json=test_data,
            headers=headers
        )
        
        print("📥 SERVER RESPONSE (THIS IS WHERE YOU SEE THE OUTPUT):")
        print("=" * 60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! Here's your honeypot output:")
            print("-" * 30)
            print(f"🚨 Scam Detected: {result.get('scamDetected', False)}")
            print(f"💬 Agent Reply: {result.get('reply', 'No reply')}")
            print(f"🆔 Session ID: {result.get('sessionId', 'N/A')}")
            print("-" * 30)
            
            # Show what this means
            print("\n📊 WHAT THIS TELLS YOU:")
            print(f"• Scam Detection: {'✅ Working' if result.get('scamDetected') else '❌ Not Working'}")
            print(f"• Agent Response: {'✅ Generated' if result.get('reply') else '❌ Missing'}")
            print(f"• Session Management: {'✅ Working' if result.get('sessionId') else '❌ Broken'}")
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Error Details: {response.text}")
            
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("Make sure your server is running!")

if __name__ == "__main__":
    test_honeypot_and_show_output()
