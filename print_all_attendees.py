#!/usr/bin/env python3
"""
Print ALL 101 attendees from the TEDxYola database
"""

import sqlite3
import os

def print_all_attendees():
    """Print all attendees in the database"""
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
        
        print("🎪 TEDxYola Event - Complete Attendees List")
        print("=" * 80)
        print(f"Total Attendees: {len(attendees)}")
        print("=" * 80)
        
        for i, (id, event_id, name, email, location, checked_in, checked_in_time) in enumerate(attendees, 1):
            status_emoji = "✅" if checked_in else "⏳"
            status_text = "CHECKED IN" if checked_in else "NOT CHECKED IN"
            
            print(f"\n{i:3d}. {status_emoji} {name}")
            print(f"     Event ID: {event_id}")
            print(f"     Email: {email}")
            print(f"     Location: {location}")
            print(f"     Status: {status_text}")
            if checked_in_time:
                print(f"     Check-in Time: {checked_in_time}")
        
        print("\n" + "=" * 80)
        print(f"✅ Listed all {len(attendees)} attendees successfully!")
        
        # Summary statistics
        checked_in_count = sum(1 for attendee in attendees if attendee[5])
        not_checked_in_count = len(attendees) - checked_in_count
        
        print(f"\n📊 Summary:")
        print(f"   Total: {len(attendees)}")
        print(f"   Checked In: {checked_in_count}")
        print(f"   Not Checked In: {not_checked_in_count}")
        print(f"   Check-in Rate: {(checked_in_count/len(attendees)*100):.1f}%")
        
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    print_all_attendees()
