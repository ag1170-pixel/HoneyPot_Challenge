import requests
import json

# Test data
test_data = {
    "sessionId": "test-session",
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

try:
    response = requests.post(
        "http://127.0.0.1:8000/honeypot/message",
        json=test_data,
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
except Exception as e:
    print(f"Error: {e}")
