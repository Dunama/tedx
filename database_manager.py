#!/usr/bin/env python3
"""
TEDxYola Database Management Utility
Complete database management script for TEDxYola event
"""

import sqlite3
import csv
import json
from datetime import datetime
import os

class TEDxDatabaseManager:
    def __init__(self, db_path="instance/tedx.db"):
        """Initialize database manager"""
        self.db_path = db_path
        print(f"🎪 TEDxYola Database Manager")
        print(f"Database: {self.db_path}")
        print("=" * 60)
    
    def get_connection(self):
        """Get database connection"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        return sqlite3.connect(self.db_path)
    
    def get_stats(self):
        """Get comprehensive database statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Total attendees
            cursor.execute("SELECT COUNT(*) FROM events")
            total = cursor.fetchone()[0]
            
            # Checked in attendees
            cursor.execute("SELECT COUNT(*) FROM events WHERE checked_in = 1")
            checked_in = cursor.fetchone()[0]
            
            # Get unique locations
            cursor.execute("SELECT COUNT(DISTINCT location) FROM events")
            unique_locations = cursor.fetchone()[0]
            
            # Get recent check-ins
            cursor.execute("""
                SELECT COUNT(*) FROM events 
                WHERE checked_in = 1 AND checked_in_time >= datetime('now', '-1 hour')
            """)
            recent_checkins = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_attendees': total,
                'checked_in': checked_in,
                'not_checked_in': total - checked_in,
                'check_in_rate': (checked_in / total * 100) if total > 0 else 0,
                'unique_locations': unique_locations,
                'recent_checkins': recent_checkins,
                'has_101_attendees': total == 101
            }
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None
    
    def export_csv(self, filename=None):
        """Export all attendees to CSV"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tedx_attendees_export_{timestamp}.csv"
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, event_id, name, email, location, checked_in, checked_in_time
                FROM events ORDER BY name
            """)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow([
                    'ID', 'Event ID', 'Name', 'Email', 'Location', 
                    'Checked In', 'Check-in Time'
                ])
                
                # Write data
                for row in cursor.fetchall():
                    checked_status = 'Yes' if row[5] else 'No'
                    checkin_time = row[6] if row[6] else ''
                    
                    writer.writerow([
                        row[0], row[1], row[2], row[3], row[4], 
                        checked_status, checkin_time
                    ])
            
            conn.close()
            print(f"✅ CSV export completed: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ CSV export failed: {e}")
            return None
    
    def export_json(self, filename=None):
        """Export all attendees to JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tedx_attendees_export_{timestamp}.json"
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, event_id, name, email, location, checked_in, checked_in_time
                FROM events ORDER BY name
            """)
            
            attendees = []
            for row in cursor.fetchall():
                attendees.append({
                    'id': row[0],
                    'event_id': row[1],
                    'name': row[2],
                    'email': row[3],
                    'location': row[4],
                    'checked_in': bool(row[5]),
                    'checked_in_time': row[6]
                })
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'total_attendees': len(attendees),
                'attendees': attendees
            }
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
            
            conn.close()
            print(f"✅ JSON export completed: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ JSON export failed: {e}")
            return None
    
    def search_attendee(self, search_term):
        """Search for attendees"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, event_id, email, location, checked_in, checked_in_time
                FROM events 
                WHERE LOWER(name) LIKE LOWER(?) OR LOWER(event_id) LIKE LOWER(?)
                ORDER BY name
            """, (f"%{search_term}%", f"%{search_term}%"))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                print(f"\n🔍 Search results for '{search_term}' ({len(results)} found):")
                print("-" * 80)
                for i, row in enumerate(results, 1):
                    status = "✅ Checked In" if row[4] else "⏳ Not Checked In"
                    print(f"{i}. {row[0]}")
                    print(f"   Event ID: {row[1]}")
                    print(f"   Email: {row[2]}")
                    print(f"   Location: {row[3]}")
                    print(f"   Status: {status}")
                    if row[5]:
                        print(f"   Check-in Time: {row[5]}")
                    print()
            else:
                print(f"❌ No attendees found matching '{search_term}'")
            
            return len(results)
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return 0
    
    def list_attendees(self, limit=10, show_checked_in_only=False):
        """List attendees with optional filters"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if show_checked_in_only:
                query = """
                    SELECT name, event_id, email, checked_in_time
                    FROM events 
                    WHERE checked_in = 1
                    ORDER BY checked_in_time DESC
                    LIMIT ?
                """
                print(f"\n👥 Checked-in attendees (last {limit}):")
            else:
                query = """
                    SELECT name, event_id, email, checked_in
                    FROM events 
                    ORDER BY name 
                    LIMIT ?
                """
                print(f"\n👥 All attendees (first {limit}):")
            
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            
            print("-" * 80)
            for i, row in enumerate(results, 1):
                if show_checked_in_only:
                    print(f"{i}. {row[0]} | {row[1]} | {row[2]} | {row[3]}")
                else:
                    status = "✅" if row[3] else "⏳"
                    print(f"{i}. {status} {row[0]} | {row[1]} | {row[2]}")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Error listing attendees: {e}")
    
    def list_all_attendees(self):
        """List ALL attendees without limit"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, event_id, name, email, location, checked_in, checked_in_time
                FROM events 
                ORDER BY name
            """)
            
            results = cursor.fetchall()
            conn.close()
            
            print(f"\n🎪 TEDxYola - Complete Attendees List")
            print("=" * 100)
            print(f"Total Attendees: {len(results)}")
            print("=" * 100)
            
            for i, (id, event_id, name, email, location, checked_in, checked_in_time) in enumerate(results, 1):
                status_emoji = "✅" if checked_in else "⏳"
                status_text = "CHECKED IN" if checked_in else "NOT CHECKED IN"
                
                print(f"\n{i:3d}. {status_emoji} {name}")
                print(f"     Event ID: {event_id}")
                print(f"     Email: {email}")
                print(f"     Location: {location}")
                print(f"     Status: {status_text}")
                if checked_in_time:
                    print(f"     Check-in Time: {checked_in_time}")
            
            print("\n" + "=" * 100)
            print(f"✅ Listed all {len(results)} attendees successfully!")
            
            # Summary statistics
            checked_in_count = sum(1 for attendee in results if attendee[5])
            not_checked_in_count = len(results) - checked_in_count
            
            print(f"\n📊 Summary:")
            print(f"   Total: {len(results)}")
            print(f"   Checked In: {checked_in_count}")
            print(f"   Not Checked In: {not_checked_in_count}")
            print(f"   Check-in Rate: {(checked_in_count/len(results)*100) if results else 0:.1f}%")
            
        except Exception as e:
            print(f"❌ Error listing all attendees: {e}")
    
    def verify_101_attendees(self):
        """Check if database has exactly 101 attendees"""
        stats = self.get_stats()
        if not stats:
            return False
        
        print(f"\n📊 Database Status Check:")
        print(f"Total attendees: {stats['total_attendees']}")
        print(f"Checked-in attendees: {stats['checked_in']}")
        print(f"Not checked-in: {stats['not_checked_in']}")
        print(f"Check-in rate: {stats['check_in_rate']:.1f}%")
        print(f"Unique locations: {stats['unique_locations']}")
        print(f"Recent check-ins (last hour): {stats['recent_checkins']}")
        
        if stats['has_101_attendees']:
            print("✅ Database has exactly 101 attendees - PERFECT!")
        elif stats['total_attendees'] < 101:
            missing = 101 - stats['total_attendees']
            print(f"⚠️  Missing {missing} attendees to reach 101")
        else:
            extra = stats['total_attendees'] - 101
            print(f"⚠️  {extra} extra attendees beyond 101")
        
        return stats['has_101_attendees']


def main():
    """Main interactive menu"""
    db_manager = TEDxDatabaseManager()
    
    # Initial check
    db_manager.verify_101_attendees()
    
    while True:
        print(f"\n📋 Database Management Menu:")
        print("1. Check attendee count and stats")
        print("2. Export to CSV")
        print("3. Export to JSON")
        print("4. Search attendee")
        print("5. List all attendees")
        print("6. List checked-in attendees")
        print("7. List ALL 101 attendees (complete list)")
        print("8. Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            db_manager.verify_101_attendees()
        
        elif choice == '2':
            filename = db_manager.export_csv()
            if filename:
                print(f"📁 CSV file saved: {filename}")
        
        elif choice == '3':
            filename = db_manager.export_json()
            if filename:
                print(f"📁 JSON file saved: {filename}")
        
        elif choice == '4':
            search_term = input("Enter name or event ID to search: ").strip()
            if search_term:
                db_manager.search_attendee(search_term)
        
        elif choice == '5':
            try:
                limit = int(input("How many attendees to show? (default 10): ") or "10")
                db_manager.list_attendees(limit)
            except ValueError:
                db_manager.list_attendees(10)
        
        elif choice == '6':
            try:
                limit = int(input("How many checked-in attendees to show? (default 10): ") or "10")
                db_manager.list_attendees(limit, show_checked_in_only=True)
            except ValueError:
                db_manager.list_attendees(10, show_checked_in_only=True)
        
        elif choice == '7':
            print("📋 Listing ALL attendees (this may take a moment)...")
            db_manager.list_all_attendees()
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
