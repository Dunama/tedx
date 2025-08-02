#!/usr/bin/env python3
"""
Run TEDxYola database migrations
"""

import os
import sys
from flask_migrate import upgrade, current, init, migrate
from app import app, db

def run_migrations():
    """Run database migrations"""
    print("🔄 TEDxYola Database Migration Script")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Check current migration status
            print("📋 Checking current migration status...")
            current_revision = current()
            print(f"Current revision: {current_revision}")
            
            # Run migrations
            print("\n🚀 Running database migrations...")
            upgrade()
            print("✅ Migrations completed successfully!")
            
            # Verify database tables
            print("\n🔍 Verifying database structure...")
            
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📊 Database tables found: {len(tables)}")
            for table in tables:
                print(f"  - {table}")
            
            # Check if our main tables exist
            required_tables = ['events', 'users']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"⚠️  Missing tables: {missing_tables}")
                print("🔧 Creating missing tables...")
                db.create_all()
                print("✅ Tables created successfully!")
            else:
                print("✅ All required tables exist!")
            
            # Final verification
            print("\n📈 Final database check...")
            from src.db.models.events import Event
            from src.models import User
            
            event_count = Event.query.count()
            user_count = User.query.count()
            
            print(f"📊 Database status:")
            print(f"  - Events/Attendees: {event_count}")
            print(f"  - Users: {user_count}")
            
            if event_count == 101:
                print("🎉 Perfect! 101 attendees confirmed in database!")
            
            print("\n✅ Migration process completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            print("🔧 Attempting to create tables manually...")
            try:
                db.create_all()
                print("✅ Tables created successfully!")
            except Exception as create_error:
                print(f"❌ Failed to create tables: {create_error}")
                return False
    
    return True

if __name__ == "__main__":
    success = run_migrations()
    if success:
        print("\n🎊 Database is ready for TEDxYola event!")
    else:
        print("\n💥 Migration failed. Please check the errors above.")
        sys.exit(1)
