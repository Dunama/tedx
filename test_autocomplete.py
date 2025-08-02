#!/usr/bin/env python3
"""
Test script to verify the autocomplete functionality
"""

import requests
import json

def test_autocomplete_search(base_url="http://localhost:5000"):
    """Test the autocomplete search functionality"""
    
    # Test cases for different search patterns
    test_queries = [
        "john",      # Common name
        "j",         # Single letter (should return empty)
        "doe",       # Last name
        "gst-",      # Event ID pattern
        "JOHN",      # Uppercase (should be case insensitive)
        "xyz123"     # Non-existent entry
    ]
    
    print("🔍 Testing Autocomplete Search Functionality")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Testing query: '{query}'")
        
        try:
            response = requests.get(f"{base_url}/registration/search", 
                                  params={'q': query})
            
            if response.status_code == 200:
                data = response.json()
                attendees = data.get('attendees', [])
                
                print(f"✅ Status: {response.status_code}")
                print(f"📊 Results: {len(attendees)} attendees found")
                
                if attendees:
                    print("👥 Found attendees:")
                    for i, attendee in enumerate(attendees[:3], 1):  # Show first 3
                        status = "✅ Checked In" if attendee.get('checked_in') else "⏳ Not Checked In"
                        print(f"   {i}. {attendee['name']} ({attendee['event_id']}) - {status}")
                    
                    if len(attendees) > 3:
                        print(f"   ... and {len(attendees) - 3} more")
                else:
                    print("❌ No attendees found")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.ConnectionError:
            print(f"❌ Cannot connect to {base_url}")
            print("   Make sure the Flask app is running")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Autocomplete Test")
    print("Make sure your Flask app is running on http://localhost:5000")
    print()
    
    test_autocomplete_search()
    
    print("\n" + "=" * 50)
    print("✨ Test completed!")
    print("\n💡 Tips for testing:")
    print("   1. Start the Flask app: python app.py")
    print("   2. Open http://localhost:5000/admin/users in your browser")
    print("   3. Try typing in the 'Enter Attendee Name' field")
    print("   4. You should see autocomplete suggestions as you type")
