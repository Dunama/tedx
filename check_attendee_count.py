#!/usr/bin/env python3
"""
Quick script to check attendee count in TEDxYola database
"""

import sqlite3
import os
from datetime import datetime

def check_database():
    """Check the database for attendee count"""
    db_path = "instance/tedx.db"
    
    print("🎪 TEDxYola Database Attendee Check")
    print("=" * 50)
    print(f"Checking database: {db_path}")
    print(f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Make sure you're running this from the TEDxYola directory")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if events table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        if not cursor.fetchone():
            print("❌ Events table not found in database")
            conn.close()
            return
        
        # Get total attendee count
        cursor.execute("SELECT COUNT(*) FROM events")
        total_count = cursor.fetchone()[0]
        
        # Get checked-in count
        cursor.execute("SELECT COUNT(*) FROM events WHERE checked_in = 1")
        checked_in_count = cursor.fetchone()[0]
        
        # Get sample attendees
        cursor.execute("SELECT name, event_id, email FROM events LIMIT 5")
        sample_attendees = cursor.fetchall()
        
        conn.close()
        
        # Display results
        print("📊 Database Status:")
        print(f"Total attendees: {total_count}")
        print(f"Checked-in attendees: {checked_in_count}")
        
        if total_count > 0:
            check_in_rate = (checked_in_count / total_count) * 100
            print(f"Check-in rate: {check_in_rate:.1f}%")
        else:
            print("Check-in rate: 0%")
        
        print()
        
        # Check if we have exactly 101 attendees
        if total_count == 101:
            print("✅ PERFECT! Database has exactly 101 attendees!")
        elif total_count < 101:
            missing = 101 - total_count
            print(f"⚠️  Database has {total_count} attendees")
            print(f"   Missing {missing} attendees to reach 101")
        else:
            extra = total_count - 101
            print(f"⚠️  Database has {total_count} attendees")
            print(f"   {extra} extra attendees beyond 101")
        
        # Show sample attendees
        if sample_attendees:
            print(f"\n👥 Sample attendees (first 5):")
            print("-" * 60)
            for i, (name, event_id, email) in enumerate(sample_attendees, 1):
                print(f"{i}. {name}")
                print(f"   ID: {event_id}")
                print(f"   Email: {email}")
                print()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    check_database()
