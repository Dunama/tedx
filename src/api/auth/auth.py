from flask import Blueprint, redirect, url_for, render_template, session, flash
from authlib.integrations.flask_client import OAuth
import os

# Initialize OAuth and Blueprint
oauth = OAuth()
auth_bp = Blueprint('auth', __name__)

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        "myApp",
        client_id=os.getenv("OAUTH2_CLIENT_ID"),    
        client_secret=os.getenv("OAUTH2_CLIENT_SECRET"), 
        server_metadata_url=os.getenv("OAUTH2_METADATA_URL"),
        client_kwargs={
            "scope": "openid email profile"
        }
    )


@auth_bp.route("/")
def signup():
    '''signup page'''
    return render_template("signup.html")

@auth_bp.route("/googleLogin")
def googleLogin():
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("auth.googleCallback", _external=True))        

@auth_bp.route("/signin-google")
def googleCallback():
    '''redirect after google oauth - FIX TO SAVE ALL USERS'''
    try:
        # Get the token from OAuth2
        token = oauth.myApp.authorize_access_token()
        
        # Extract user information from the token
        user_info = token.get('userinfo')
        if not user_info:
            print("No userinfo in token")
            flash('Failed to get user information from Google')
            return redirect(url_for("auth.signup"))
        
        # Get email from user info
        email = user_info.get('email')
        name = user_info.get('name', '')
        
        print(f"OAuth Callback - Processing user: {email}")  # Debug log
        
        if not email:
            print("No email found in userinfo")
            flash('Email not provided by Google')
            return redirect(url_for("auth.signup"))
        
        # Save user to dummy_db for admin panel visibility
        try:
            from src.api.auth.dummy_db import dummy_db
            # Check if user already exists in dummy_db
            exists = False
            for user in getattr(dummy_db, 'users', []):
                if (isinstance(user, dict) and user.get('email') == email) or \
                   (hasattr(user, 'email') and getattr(user, 'email', None) == email):
                    exists = True
                    break
            if not exists:
                new_id = len(getattr(dummy_db, 'users', [])) + 1
                dummy_db.users.append({'id': new_id, 'email': email})
                print(f"Added {email} to dummy_db.users")
        except Exception as e:
            print(f"Could not save user to dummy_db: {e}")

        # Store user data in session (this is what makes login work)
        session["user"] = {
            'email': email,
            'name': name,
            'userinfo': user_info
        }
        
        # Store the full token for potential future use
        session["token"] = token
        
        print(f"Session created for user: {email}")
        return redirect(url_for("auth.login"))
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        flash('Authentication failed. Please try again.')
        return redirect(url_for("auth.signup"))

@auth_bp.route('/login')
def login():
    user = session.get("user")
    return render_template("login.html", user=user)

# Dummy User class for database operations (replace with your actual User model)
class User:
    def __init__(self, email, is_pro=False):
        self.email = email
        self.is_pro = is_pro
    
    @staticmethod
    def query():
        return UserQuery()

class UserQuery:
    def filter_by(self, **kwargs):
        return self
    
    def first(self):
        return None

# Dummy database session (replace with your actual db session)
class DBSession:
    def add(self, obj):
        pass
    
    def commit(self):
        pass
    
    def rollback(self):
        pass

db = type('DB', (), {'session': DBSession()})()

