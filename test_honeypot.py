#!/usr/bin/env python3
"""
Test script to validate honeypot scam detection functionality.
Tests various scam scenarios and measures detection accuracy.
"""

import json
import requests
from datetime import datetime
from test_data import TEST_SCENARIOS, EDGE_CASES, generate_test_request, generate_conversation_test
from handler import detect_scam, extract_intelligence, agent_reply
from models import SessionState

def test_detection_function():
    """Test the scam detection function directly."""
    print("=== TESTING SCAM DETECTION FUNCTION ===")
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for category, tests in TEST_SCENARIOS.items():
        print(f"\n--- Testing {category.upper()} ---")
        
        for test in tests:
            total_tests += 1
            result = detect_scam(test['message'], [])
            
            # Check if scam detection matches expectation
            scam_match = result.scamDetected == test['expected_scam']
            
            # Check if confidence is within reasonable range
            confidence_ok = abs(result.confidence - test['expected_confidence']) <= 0.2
            
            if scam_match and confidence_ok:
                passed_tests += 1
                status = "✓ PASS"
            else:
                failed_tests.append({
                    'test': test['name'],
                    'category': category,
                    'expected_scam': test['expected_scam'],
                    'actual_scam': result.scamDetected,
                    'expected_confidence': test['expected_confidence'],
                    'actual_confidence': result.confidence
                })
                status = "✗ FAIL"
            
            print(f"{status} {test['name']}: Scam={result.scamDetected}, Confidence={result.confidence:.2f}")
            if result.reasons:
                print(f"    Reasons: {result.reasons[:3]}")  # Show first 3 reasons
    
    print(f"\n--- EDGE CASES ---")
    for test in EDGE_CASES:
        total_tests += 1
        result = detect_scam(test['message'], [])
        
        scam_match = result.scamDetected == test['expected_scam']
        confidence_ok = abs(result.confidence - test['expected_confidence']) <= 0.2
        
        if scam_match and confidence_ok:
            passed_tests += 1
            status = "✓ PASS"
        else:
            failed_tests.append({
                'test': test['name'],
                'category': 'edge_cases',
                'expected_scam': test['expected_scam'],
                'actual_scam': result.scamDetected,
                'expected_confidence': test['expected_confidence'],
                'actual_confidence': result.confidence
            })
            status = "✗ FAIL"
        
        print(f"{status} {test['name']}: Scam={result.scamDetected}, Confidence={result.confidence:.2f}")
    
    print(f"\n=== DETECTION TEST SUMMARY ===")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Accuracy: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests:
        print("\n--- FAILED TESTS ---")
        for fail in failed_tests:
            print(f"{fail['test']} ({fail['category']})")
            print(f"  Expected: Scam={fail['expected_scam']}, Conf={fail['expected_confidence']}")
            print(f"  Actual: Scam={fail['actual_scam']}, Conf={fail['actual_confidence']:.2f}")
    
    return passed_tests, total_tests

def test_intelligence_extraction():
    """Test intelligence extraction functionality."""
    print("\n=== TESTING INTELLIGENCE EXTRACTION ===")
    
    test_cases = [
        {
            "name": "UPI Extraction",
            "message": "Send money to user@bank and winner@upi",
            "expected_upi": ["user@bank", "winner@upi"]
        },
        {
            "name": "Phone Extraction",
            "message": "Call +919876543210 or 01123456789 or 8877665544",
            "expected_phones": ["+919876543210", "01123456789", "8877665544"]
        },
        {
            "name": "URL Extraction",
            "message": "Visit http://bit.ly/scam and https://tinyurl.com/fake",
            "expected_urls": ["http://bit.ly/scam", "https://tinyurl.com/fake"]
        },
        {
            "name": "Bank Account Extraction",
            "message": "Account number 1234567890123456 for transfer",
            "expected_accounts": ["1234567890123456"]
        },
        {
            "name": "Keywords Extraction",
            "message": "URGENT payment required immediately",
            "expected_keywords": ["urgent", "payment", "immediately"]
        }
    ]
    
    total_tests = len(test_cases)
    passed_tests = 0
    
    for test in test_cases:
        intelligence = {}
        result = extract_intelligence(test['message'], intelligence)
        
        test_passed = True
        
        if 'expected_upi' in test:
            actual_upi = set(result.get('upi_ids', []))
            expected_upi = set(test['expected_upi'])
            if actual_upi != expected_upi:
                test_passed = False
                print(f"✗ UPI mismatch: expected {expected_upi}, got {actual_upi}")
        
        if 'expected_phones' in test:
            actual_phones = set(result.get('phone_numbers', []))
            expected_phones = set(test['expected_phones'])
            if actual_phones != expected_phones:
                test_passed = False
                print(f"✗ Phone mismatch: expected {expected_phones}, got {actual_phones}")
        
        if 'expected_urls' in test:
            actual_urls = set(result.get('urls', []))
            expected_urls = set(test['expected_urls'])
            if actual_urls != expected_urls:
                test_passed = False
                print(f"✗ URL mismatch: expected {expected_urls}, got {actual_urls}")
        
        if 'expected_accounts' in test:
            actual_accounts = set(result.get('bank_accounts', []))
            expected_accounts = set(test['expected_accounts'])
            if actual_accounts != expected_accounts:
                test_passed = False
                print(f"✗ Account mismatch: expected {expected_accounts}, got {actual_accounts}")
        
        if 'expected_keywords' in test:
            actual_keywords = set(result.get('suspicious_keywords', []))
            expected_keywords = set(test['expected_keywords'])
            if not expected_keywords.issubset(actual_keywords):
                test_passed = False
                print(f"✗ Keywords mismatch: expected {expected_keywords}, got {actual_keywords}")
        
        if test_passed:
            passed_tests += 1
            print(f"✓ PASS {test['name']}")
        else:
            print(f"✗ FAIL {test['name']}")
    
    print(f"\nIntelligence Extraction: {passed_tests}/{total_tests} passed ({(passed_tests/total_tests)*100:.1f}%)")
    return passed_tests, total_tests

def test_agent_replies():
    """Test agent reply generation."""
    print("\n=== TESTING AGENT REPLIES ===")
    
    test_scenarios = [
        {
            "name": "Payment Request Response",
            "last_message": "Please send ₹5000 to claim your prize",
            "expected_contains": ["carefully", "details", "payment"]
        },
        {
            "name": "Personal Info Request Response", 
            "last_message": "Share your account number for verification",
            "expected_contains": ["comfortable", "information", "why"]
        },
        {
            "name": "Urgency Response",
            "last_message": "ACT NOW OR LOSE EVERYTHING!!!",
            "expected_contains": ["time", "understand", "slow"]
        },
        {
            "name": "General Response",
            "last_message": "Hello, how are you?",
            "expected_contains": ["explain", "understand", "help"]
        }
    ]
    
    total_tests = len(test_scenarios)
    passed_tests = 0
    
    for test in test_scenarios:
        # Create a mock session state
        session_state = SessionState(
            conversation_history=[{"text": test['last_message'], "sender": "scammer", "timestamp": datetime.now().isoformat()}],
            scam_detected=True,
            total_message_count=1,
            extracted_intelligence={},
            consecutive_no_new_intel=0
        )
        
        reply = agent_reply(session_state)
        
        # Check if reply contains expected keywords
        reply_lower = reply.lower()
        contains_expected = any(keyword in reply_lower for keyword in test['expected_contains'])
        
        # Check if reply follows rules (no prohibited words)
        prohibited_words = ['scam', 'fraud', 'report', 'police', 'illegal']
        contains_prohibited = any(word in reply_lower for word in prohibited_words)
        
        # Check if it asks at most one question
        question_count = reply.count('?')
        
        if contains_expected and not contains_prohibited and question_count <= 1:
            passed_tests += 1
            print(f"✓ PASS {test['name']}: {reply}")
        else:
            print(f"✗ FAIL {test['name']}: {reply}")
            if not contains_expected:
                print(f"  Missing expected keywords: {test['expected_contains']}")
            if contains_prohibited:
                print(f"  Contains prohibited words: {prohibited_words}")
            if question_count > 1:
                print(f"  Too many questions: {question_count}")
    
    print(f"\nAgent Replies: {passed_tests}/{total_tests} passed ({(passed_tests/total_tests)*100:.1f}%)")
    return passed_tests, total_tests

def test_conversation_flow():
    """Test multi-message conversation flow."""
    print("\n=== TESTING CONVERSATION FLOW ===")
    
    conversation = generate_conversation_test()
    session_state = SessionState(
        conversation_history=[],
        scam_detected=False,
        total_message_count=0,
        extracted_intelligence={},
        consecutive_no_new_intel=0
    )
    
    for i, step in enumerate(conversation):
        print(f"\n--- Step {i+1}: {step['name']} ---")
        
        # Add message to conversation
        session_state.conversation_history.append({
            "text": step['message'],
            "sender": "scammer",
            "timestamp": datetime.now().isoformat()
        })
        session_state.total_message_count += 1
        
        # Test scam detection
        result = detect_scam(step['message'], session_state.conversation_history)
        print(f"Scam Detection: {result.scamDetected} (Confidence: {result.confidence:.2f})")
        
        # Update session state if scam detected
        if result.scamDetected and not session_state.scam_detected:
            session_state.scam_detected = True
            print("Scam detected for the first time!")
        
        # Test intelligence extraction
        if session_state.scam_detected:
            new_intel = extract_intelligence(step['message'], session_state.extracted_intelligence)
            session_state.extracted_intelligence = new_intel
            print(f"Extracted Intelligence: {session_state.extracted_intelligence}")
            
            # Test agent reply
            reply = agent_reply(session_state)
            print(f"Agent Reply: {reply}")
        else:
            print("No scam detected yet - using safe reply")
    
    print(f"\nFinal Session State:")
    print(f"Total Messages: {session_state.total_message_count}")
    print(f"Scam Detected: {session_state.scam_detected}")
    print(f"Extracted Intelligence: {session_state.extracted_intelligence}")

def run_api_tests(base_url="http://127.0.0.1:8000"):
    """Run tests against the live API."""
    print("\n=== TESTING LIVE API ===")
    
    try:
        # Test health endpoint
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code == 200:
            print("✓ API is running and healthy")
        else:
            print("✗ API health check failed")
            return
    except requests.exceptions.RequestException:
        print("✗ Cannot connect to API. Make sure the server is running.")
        return
    
    # Test a few sample messages
    sample_tests = [
        {
            "name": "Bank Scam API Test",
            "message": "URGENT: Your account will be suspended! Call +919876543210 now!"
        },
        {
            "name": "Safe Message API Test", 
            "message": "Hello, how are you today?"
        }
    ]
    
    for test in sample_tests:
        print(f"\n--- {test['name']} ---")
        
        request_data = generate_test_request(f"api-test-{test['name']}", test['message'])
        
        try:
            response = requests.post(
                f"{base_url}/honeypot/message",
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✓ API Response: {result}")
            else:
                print(f"✗ API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Request failed: {e}")

def main():
    """Run all tests."""
    print("🍯 HONEYPOT SCAM DETECTION TEST SUITE 🍯")
    print("=" * 50)
    
    # Run individual function tests
    detection_passed, detection_total = test_detection_function()
    intel_passed, intel_total = test_intelligence_extraction()
    reply_passed, reply_total = test_agent_replies()
    
    # Run conversation flow test
    test_conversation_flow()
    
    # Run API tests (optional)
    run_api_tests()
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 50)
    
    total_function_tests = detection_total + intel_total + reply_total
    total_passed = detection_passed + intel_passed + reply_passed
    
    print(f"Detection Tests: {detection_passed}/{detection_total} ({(detection_passed/detection_total)*100:.1f}%)")
    print(f"Intelligence Tests: {intel_passed}/{intel_total} ({(intel_passed/intel_total)*100:.1f}%)")
    print(f"Reply Tests: {reply_passed}/{reply_total} ({(reply_passed/reply_total)*100:.1f}%)")
    print(f"Overall: {total_passed}/{total_function_tests} ({(total_passed/total_function_tests)*100:.1f}%)")
    
    if total_passed == total_function_tests:
        print("\n🎉 ALL TESTS PASSED! Your honeypot is working correctly!")
    else:
        print(f"\n⚠️  {total_function_tests - total_passed} tests failed. Review the failures above.")

if __name__ == "__main__":
    main()
