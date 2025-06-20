from flask import Blueprint, jsonify, request, make_response
from datetime import datetime

# Import your User model and db session here
from src.api.auth.auth import User, db
from src.api.auth.dummy_db import dummy_db

# Create admin blueprint for administrative functions
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def get_all_oauth_users():
    """
    Admin function to retrieve all users who signed up with Google OAuth2
    
    Returns:
        dict: Contains user data and summary statistics
    """
    try:
        # Fetch users from dummy_db instead of database
        all_users = getattr(dummy_db, 'users', [])
        print(f"DEBUG: Dummy DB query returned {len(all_users)} users")  # Debug log
        
        # Create a list to store user information
        user_data = []
        
        # Loop through each user and extract relevant information
        for user in all_users:
            user_info = {
                'id': user.get('id', None),
                'email': user.get('email', None),
                'registration_method': 'Google OAuth2'
            }
            user_data.append(user_info)
            print(f"DEBUG: Found user {user_info['id']}: {user_info['email']}")  # Debug log
        
        total_users = len(user_data)
        print(f"DEBUG: Total users: {total_users}")  # Debug log
        
        # Return comprehensive user data with statistics
        return {
            'success': True,
            'total_users': total_users,
            'users': user_data,
            'generated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        # Handle any database or processing errors
        print(f"ERROR in get_all_oauth_users: {e}")  # Debug log
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve user data'
        }

# @admin_bp.route('/users')
# def view_all_users():
#     """
#     Admin route to display all OAuth2 users in a web interface
    
#     This endpoint provides a simple HTML view of all registered users
#     Access: GET /admin/users
#     """
#     # Get all user data using our admin function
#     user_data = get_all_oauth_users()
    
#     # Check if data retrieval was successful
#     if not user_data['success']:
#         return jsonify({
#             'error': 'Unable to fetch user data',
#             'details': user_data.get('error', 'Unknown error')
#         }), 500
        
    
#     # Get user data and return as JSON
#     user_data = get_all_oauth_users()
    
#     # Return JSON response with appropriate status code
#     if user_data['success']:
#         return jsonify(user_data), 200
#     else:
#         return jsonify(user_data), 500

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
