from flask import Blueprint, jsonify, render_template_string, request, make_response
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

@admin_bp.route('/users')
def view_all_users():
    """
    Admin route to display all OAuth2 users in a web interface
    
    This endpoint provides a simple HTML view of all registered users
    Access: GET /admin/users
    """
    # Get all user data using our admin function
    user_data = get_all_oauth_users()
    
    # Check if data retrieval was successful
    if not user_data['success']:
        return jsonify({
            'error': 'Unable to fetch user data',
            'details': user_data.get('error', 'Unknown error')
        }), 500
        
    # Enhanced HTML template with TEDxYola branding and existing fonts
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TEDxYola - Admin Dashboard</title>
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body { 
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
                line-height: 1.6;
            }
            
            .container { 
                max-width: 1400px; 
                margin: 0 auto; 
                background: white; 
                min-height: 100vh;
                box-shadow: 0 0 50px rgba(0,0,0,0.1); 
            }
            
            .header { 
                background: linear-gradient(135deg, #E62B1E 0%, #FF4136 100%);
                color: white; 
                text-align: center; 
                padding: 40px 20px;
                position: relative;
                overflow: hidden;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="3" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
                animation: float 20s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            
            .header h1 { 
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 10px;
                position: relative;
                z-index: 1;
            }
            
            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }
            
            .content {
                padding: 40px;
            }
            
            .debug-section { 
                background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                border: 1px solid #ffeaa7; 
                padding: 25px; 
                margin-bottom: 30px; 
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .debug-section h4 { 
                margin-top: 0; 
                color: #856404;
                font-size: 1.3rem;
                font-weight: 600;
            }
            
            .stats { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 30px; 
                border-radius: 20px; 
                margin-bottom: 40px;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            }
            
            .stats h3 { 
                margin-top: 0; 
                color: white;
                font-size: 1.8rem;
                font-weight: 600;
                margin-bottom: 20px;
            }
            
            .stat-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-top: 20px; 
            }
            
            .stat-item { 
                background: rgba(255,255,255,0.2); 
                padding: 25px; 
                border-radius: 15px; 
                text-align: center;
                backdrop-filter: blur(10px);
                transition: transform 0.3s ease;
            }
            
            .stat-item:hover {
                transform: translateY(-5px);
            }
            
            .stat-number { 
                font-size: 2.5rem; 
                font-weight: 700;
                display: block;
                margin-bottom: 5px;
            }
            
            .stat-label { 
                font-size: 1rem; 
                opacity: 0.9;
                font-weight: 500;
            }
            
            .controls { 
                margin-bottom: 30px; 
                text-align: center;
                display: flex;
                justify-content: center;
                gap: 15px;
                flex-wrap: wrap;
            }
            
            .btn {
                border: none; 
                padding: 15px 30px; 
                border-radius: 50px; 
                cursor: pointer; 
                font-size: 1rem;
                font-weight: 600;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }
            
            .refresh-btn { 
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            }
            
            .refresh-btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
            }
            
            .auto-refresh-btn { 
                background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
            }
            
            .auto-refresh-btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
            }
            
            .test-btn { 
                background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
            }
            
            .test-btn:hover { 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
            }
            
            .user-table { 
                width: 100%; 
                border-collapse: collapse; 
                background: white; 
                border-radius: 15px; 
                overflow: hidden; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-top: 20px;
            }
            
            .user-table th, .user-table td { 
                padding: 20px; 
                text-align: left; 
                border-bottom: 1px solid #f0f0f0; 
            }
            
            .user-table th { 
                background: linear-gradient(135deg, #E62B1E 0%, #FF4136 100%);
                color: white; 
                font-weight: 600;
                font-size: 1rem;
                position: sticky;
                top: 0;
            }
        
        
            .user-table tr:hover { 
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                transform: scale(1.01);
                transition: all 0.3s ease;
            }
            
            .no-users { 
                text-align: center; 
                padding: 60px; 
                color: #666; 
                font-style: italic;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 15px;
                margin: 20px 0;
            }
            
            .no-users h3 {
                font-size: 2rem;
                margin-bottom: 20px;
                color: #E62B1E;
            }
            
            .last-updated { 
                text-align: center; 
                margin-top: 30px; 
                color: #666; 
                font-size: 0.9rem;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            
            .auto-refresh-status { 
                display: inline-block; 
                margin-left: 15px; 
                padding: 8px 16px; 
                border-radius: 25px; 
                font-size: 0.8rem;
                font-weight: 600;
            }
            
            .auto-refresh-on { 
                background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
                color: #2e7d32; 
            }
            
            .auto-refresh-off { 
                background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
                color: #c62828; 
            }
            
            .section-title {
                font-size: 1.8rem;
                font-weight: 600;
                color: #333;
                margin: 40px 0 20px 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            @media (max-width: 768px) {
                .header h1 { font-size: 2rem; }
                .content { padding: 20px; }
                .stat-grid { grid-template-columns: 1fr; }
                .controls { flex-direction: column; align-items: center; }
                .user-table { font-size: 0.9rem; }
                .user-table th, .user-table td { padding: 15px 10px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>TEDxYola</h1>
                <p>Admin Dashboard - User Management</p>
            </div>
            
            <div class="content">
                <div class="debug-section">
                    <h4>🐛 Debug Information</h4>
                    <p><strong>Total Users in Database:</strong> {{ total_users }}</p>
                    <p><strong>Query Time:</strong> {{ generated_at }}</p>
                    <p><strong>Issue:</strong> If you signed up but don't see your email here, the OAuth2 callback isn't saving users properly.</p>
                    <p><strong>Next Step:</strong> Check server logs for OAuth2 errors, or try signing up again with a new email.</p>
                </div>
                
                <!-- Display summary statistics -->
                <div class="stats">
                    <h3>📊 User Statistics</h3>
                    <div class="stat-grid">
                        <div class="stat-item">
                            <div class="stat-number">{{ total_users }}</div>
                            <div class="stat-label">Total Users</div>
                        </div>
                    </div>
                </div>
                
                <!-- Control buttons -->
                <div class="controls">
                    <button class="btn refresh-btn" onclick="refreshData()">🔄 Refresh Now</button>
                    <span id="autoRefreshStatus" class="auto-refresh-status auto-refresh-off" style="display:none;">OFF</span>
                </div>
                
                <!-- Display user table -->
                <h3 class="section-title">👥 All Registered Users</h3>
                {% if users and users|length > 0 %}
                <table class="user-table">
                    <thead>
                        <tr>
                            <th>🆔 User ID</th>
                            <th>📧 Email Address</th>
                            <th>🔐 Registration Method</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                        <tr>
                            <td>{{ user.id }}</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.registration_method }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div class="no-users">
                    <h3>😔 No users found in database</h3>
                    <p><strong>This means the OAuth2 callback is not working properly or no one has signed up yet.</strong></p>
                    <p>Users are signing up but not being saved to the database.</p>
                    <p><a href="/" target="_blank" style="color: #E62B1E; text-decoration: none; font-weight: 600;">Try signing up again</a> and check server logs for errors.</p>
                </div>
                {% endif %}
                
                <div class="last-updated">
                    📅 Last Updated: {{ generated_at }}
                </div>
            </div>
        </div>

        <script>
            function refreshData() {
                // Add timestamp to prevent caching
                const timestamp = new Date().getTime();
                window.location.href = window.location.pathname + '?t=' + timestamp;
            }

            // Prevent caching
            window.addEventListener('pageshow', function(event) {
                if (event.persisted) {
                    window.location.reload();
                }
            });
        </script>
    </body>
    </html>
    """
        
    # Render the template with user data and add cache-busting headers
    response = make_response(render_template_string(html_template, **user_data))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@admin_bp.route('/users/api')
def get_users_api():
    """
    Admin API endpoint to get all OAuth2 users as JSON
    
    This endpoint returns raw JSON data for programmatic access
    Access: GET /admin/users/api
    
    Returns:
        JSON: Complete user data with statistics
    """
    # Get user data and return as JSON
    user_data = get_all_oauth_users()
    
    # Return JSON response with appropriate status code
    if user_data['success']:
        return jsonify(user_data), 200
    else:
        return jsonify(user_data), 500

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
