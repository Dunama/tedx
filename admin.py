from flask import Blueprint, jsonify, request, make_response, send_file, Response
from datetime import datetime
import csv
import io
import tempfile
import os

# Import your User model and db session here
from src.models import User, db
from src.db.models.events import Event

# Create admin blueprint for administrative functions
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def get_all_oauth_users():
    """
    Admin function to retrieve all users who signed up with Google OAuth2
    
    Returns:
        dict: Contains user data and summary statistics
    """
    try:
        # Fetch users from the actual database
        all_users = User.get_oauth_users()
        print(f"DEBUG: Database query returned {len(all_users)} OAuth users")  # Debug log
        
        # Create a list to store user information
        user_data = []
        
        # Loop through each user and extract relevant information
        for user in all_users:
            user_info = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'registration_method': user.registration_method,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
            user_data.append(user_info)
            print(f"DEBUG: Found user {user_info['id']}: {user_info['email']}")  # Debug log
        
        total_users = len(user_data)
        total_all_users = User.get_total_users()
        print(f"DEBUG: Total OAuth users: {total_users}, Total all users: {total_all_users}")  # Debug log
        
        # Return comprehensive user data with statistics
        return {
            'success': True,
            'total_users': total_users,
            'total_all_users': total_all_users,
            'users': user_data,
            'generated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        # Handle any database or processing errors
        print(f"ERROR in get_all_oauth_users: {e}")  # Debug log
        return {
            'success': False,
            'error': str(e),
            'total_users': 0,
            'users': [],
            'generated_at': datetime.now().isoformat()
        }


@admin_bp.route('/users')
def admin_get_users():
    """
    Admin endpoint to get all OAuth users
    
    Access: GET /admin/users
    
    Returns:
        JSON: All OAuth user data with statistics
    """
    try:
        user_data = get_all_oauth_users()
        
        # Return JSON response with appropriate status code
        if user_data['success']:
            return jsonify(user_data), 200
        else:
            return jsonify(user_data), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unable to fetch user data: {str(e)}',
            'total_users': 0,
            'users': []
        }), 500


@admin_bp.route('/stats')
def get_admin_stats():
    """
    Get comprehensive admin statistics including users and events
    
    Returns:
        JSON: Complete statistics for admin dashboard
    """
    try:
        # Get user statistics
        total_users = User.get_total_users()
        oauth_users = User.get_oauth_users_count()
        
        # Get event statistics
        total_registered = Event.get_total_registered()
        checked_in = Event.get_checked_in_attendees()
        event_capacity = Event.get_event_capacity()
        checkin_rate = Event.get_checked_in_rate()
        
        return jsonify({
            'success': True,
            'user_stats': {
                'total_users': total_users,
                'oauth_users': oauth_users,
                'local_users': total_users - oauth_users
            },
            'event_stats': {
                'total_registered': total_registered,
                'checked_in': checked_in,
                'event_capacity': event_capacity,
                'checkin_rate': checkin_rate
            },
            'generated_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@admin_bp.route('/users/count')
def get_user_count():
    """
    Quick endpoint to get just the user count statistics
    
    Access: GET /admin/users/count
    
    Returns:
        JSON: User count statistics only
    """
    try:
        user_data = get_all_oauth_users()
        if user_data['success']:
            return jsonify({
                'success': True,
                'total_users': user_data['total_users']
            }), 200
        else:
            return jsonify(user_data), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Additional utility function for searching users
# def search_users_by_email(email_pattern):
#     """
#     Search for users by email pattern (for admin use)
    
#     Args:
#         email_pattern (str): Email pattern to search for
        
#     Returns:
#         list: List of matching users
#     """
#     try:
#         # For demo purposes, return empty list
#         # In real implementation, query your database here
#         return []
        
#     except Exception as e:
#         print(f"Error searching users: {e}")
#         return []


@admin_bp.route('/export/csv')
def export_csv():
    """
    Export all attendees data to CSV format
    """
    try:
        # Get all attendees from database
        attendees = Event.query.all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Event ID', 'Name', 'Email', 'Location', 
            'Checked In', 'Check-in Time'
        ])
        
        # Write data
        for attendee in attendees:
            writer.writerow([
                attendee.id,
                attendee.event_id,
                attendee.name,
                attendee.email,
                attendee.location,
                'Yes' if attendee.checked_in else 'No',
                attendee.checked_in_time.strftime('%Y-%m-%d %H:%M:%S') if attendee.checked_in_time else ''
            ])
        
        # Create response
        output.seek(0)
        response = Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=tedx_attendees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            }
        )
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Export failed: {str(e)}'
        }), 500


@admin_bp.route('/export/db-script')
def export_db_script():
    """
    Export a Python script for database management
    """
    try:
        # Get current attendee count
        total_attendees = Event.get_total_registered()
        
        # Create Python script content  
        script_content = f'''#!/usr/bin/env python3
"""
TEDxYola Database Management Script
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Current attendees in database: {total_attendees}
"""

import sqlite3
import csv
from datetime import datetime
import os

class TEDxDatabaseManager:
    def __init__(self, db_path="instance/tedx.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Ensure database file exists"""
        if not os.path.exists(self.db_path):
            print(f"Database not found at {{self.db_path}}")
            return False
        return True
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def check_attendee_count(self):
        """Check total number of attendees"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM events")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error checking attendee count: {{e}}")
            return 0
    
    def verify_101_attendees(self):
        """Check if database has exactly 101 attendees"""
        count = self.check_attendee_count()
        print(f"\\n📊 Database Status Check:")
        print(f"Total attendees: {{count}}")
        
        if count == 101:
            print("✅ Database has exactly 101 attendees - PERFECT!")
        elif count < 101:
            print(f"⚠️  Database has {{count}} attendees - Missing {{101 - count}} attendees")
        else:
            print(f"⚠️  Database has {{count}} attendees - {{count - 101}} extra attendees")
        
        return count == 101


def main():
    """Main function to check database"""
    print("🎪 TEDxYola Database Checker")
    print("=" * 50)
    
    # Initialize manager
    db_manager = TEDxDatabaseManager()
    
    # Check if we have 101 attendees
    db_manager.verify_101_attendees()


if __name__ == "__main__":
    main()
'''

        # Create response
        response = Response(
            script_content,
            mimetype='text/plain',
            headers={
                'Content-Disposition': f'attachment; filename=database_manager_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
            }
        )
        
        return response
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Script export failed: {str(e)}'
        }), 500


@admin_bp.route('/check-attendees')
def check_attendees():
    """
    Check if database has exactly 101 attendees
    """
    try:
        total_attendees = Event.get_total_registered()
        checked_in = Event.get_checked_in_attendees()
        
        return jsonify({
            'success': True,
            'total_attendees': total_attendees,
            'checked_in': checked_in,
            'has_101_attendees': total_attendees == 101,
            'difference_from_101': total_attendees - 101,
            'check_in_rate': Event.get_checked_in_rate()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
