#!/usr/bin/env python3
"""
List ALL attendees from TEDxYola database
Direct script - no menu, just prints all attendees
"""

import sqlite3
import os

def list_all_attendees_direct():
    """Print all attendees directly"""
    db_path = "instance/tedx.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all attendees ordered by name
        cursor.execute("""
            SELECT id, event_id, name, email, location, checked_in, checked_in_time
            FROM events 
            ORDER BY name
        """)
        
        attendees = cursor.fetchall()
        conn.close()
        
        print("🎪 TEDxYola Event - Complete Attendees Database")
        print("=" * 100)
        print(f"Total Attendees: {len(attendees)}")
        print("=" * 100)
        
        for i, (id, event_id, name, email, location, checked_in, checked_in_time) in enumerate(attendees, 1):
            status_emoji = "✅" if checked_in else "⏳"
            status_text = "CHECKED IN" if checked_in else "NOT CHECKED IN"
            
            print(f"\n{i:3d}. {status_emoji} {name}")
            print(f"     ID: {id}")
            print(f"     Event ID: {event_id}")
            print(f"     Email: {email}")
            print(f"     Location: {location}")
            print(f"     Status: {status_text}")
            if checked_in_time:
                print(f"     Check-in Time: {checked_in_time}")
        
        print("\n" + "=" * 100)
        print(f"✅ Complete list of all {len(attendees)} attendees displayed!")
        
        # Summary statistics
        checked_in_count = sum(1 for attendee in attendees if attendee[5])
        not_checked_in_count = len(attendees) - checked_in_count
        unique_locations = len(set(attendee[4] for attendee in attendees))
        
        print(f"\n📊 Database Summary:")
        print(f"   Total Attendees: {len(attendees)}")
        print(f"   Checked In: {checked_in_count}")
        print(f"   Not Checked In: {not_checked_in_count}")
        print(f"   Check-in Rate: {(checked_in_count/len(attendees)*100) if attendees else 0:.1f}%")
        print(f"   Unique Locations: {unique_locations}")
        print(f"   Has exactly 101 attendees: {'✅ YES' if len(attendees) == 101 else '❌ NO'}")
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    print("🚀 Starting complete attendees listing...")
    list_all_attendees_direct()
    print("\n🎉 Complete! All attendees have been listed above.")
