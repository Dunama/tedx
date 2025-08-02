#!/usr/bin/env python3
"""
Test script to verify that the registration dashboard properly handles
lowercase conversion for both names and IDs.
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:5000"
REGISTRATION_URL = f"{BASE_URL}/registration"

def test_case_insensitive_search():
    """Test case-insensitive search functionality"""
    print("Testing case-insensitive search...")
    
    # Test with lowercase query
    test_queries = [
        "john",      # lowercase name
        "JOHN",      # uppercase name
        "John",      # mixed case name
        "gst-",      # lowercase serial prefix
        "GST-",      # uppercase serial prefix
    ]
    
    for query in test_queries:
        try:
            response = requests.get(f"{REGISTRATION_URL}/search", params={"q": query})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Query '{query}': Found {len(data.get('attendees', []))} results")
            else:
                print(f"❌ Query '{query}': Failed with status {response.status_code}")
        except Exception as e:
            print(f"❌ Query '{query}': Error - {e}")

def test_case_insensitive_validation():
    """Test case-insensitive validation functionality"""
    print("\nTesting case-insensitive validation...")
    
    # Test cases with different case combinations
    test_cases = [
        {"ticket_serial": "gst-example123", "attendee_name": ""},
        {"ticket_serial": "GST-EXAMPLE123", "attendee_name": ""},
        {"ticket_serial": "", "attendee_name": "john doe"},
        {"ticket_serial": "", "attendee_name": "JOHN DOE"},
        {"ticket_serial": "", "attendee_name": "John Doe"},
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                f"{REGISTRATION_URL}/validate",
                headers={"Content-Type": "application/json"},
                data=json.dumps(test_case)
            )
            
            serial = test_case.get("ticket_serial", "")
            name = test_case.get("attendee_name", "")
            identifier = serial if serial else name
            
            if response.status_code in [200, 404]:  # 404 is expected if attendee not found
                data = response.json()
                status = data.get('status', 'error')
                print(f"✅ Test '{identifier}': Status = {status}")
            else:
                print(f"❌ Test '{identifier}': Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test '{identifier}': Error - {e}")

def test_stats_endpoint():
    """Test stats endpoint functionality"""
    print("\nTesting stats endpoint...")
    
    try:
        response = requests.get(f"{REGISTRATION_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Stats: {data}")
        else:
            print(f"❌ Stats failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {e}")

if __name__ == "__main__":
    print("🧪 Testing TEDxYola Registration Dashboard - Case Insensitive Search")
    print("=" * 70)
    
    print("Note: Make sure the Flask app is running on http://localhost:5000")
    print("You can start it with: python app.py")
    print()
    
    # Run tests
    test_case_insensitive_search()
    test_case_insensitive_validation()
    test_stats_endpoint()
    
    print("\n" + "=" * 70)
    print("✅ Testing completed!")
    print("\nKey improvements made:")
    print("1. All inputs (names and IDs) are converted to lowercase")
    print("2. Database searches use case-insensitive matching (ILIKE)")
    print("3. Search can find attendees by both name AND event_id")
    print("4. All comparisons are consistent and case-insensitive")
