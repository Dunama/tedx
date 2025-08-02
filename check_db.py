import sqlite3
import os

# Check the database file directly
db_path = 'instance/tedx.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('Tables in database:', [table[0] for table in tables])
    
    # Check events table
    table_names = [table[0] for table in tables]
    if 'events' in table_names:
        cursor.execute('SELECT COUNT(*) FROM events')
        count = cursor.fetchone()[0]
        print(f'Events table count: {count}')
        
        # Show sample data
        cursor.execute('SELECT name, event_id FROM events LIMIT 5')
        samples = cursor.fetchall()
        print('Sample events:')
        for sample in samples:
            print(f'  - {sample[0]} ({sample[1]})')
    
    # Check attendees table
    if 'attendees' in table_names:
        cursor.execute('SELECT COUNT(*) FROM attendees')
        count = cursor.fetchone()[0]
        print(f'Attendees table count: {count}')
    
    conn.close()
else:
    print('Database file not found')
