from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128))  # Optional if using OAuth only
    registration_method = db.Column(db.String(50), default='local')  # 'local' or 'oauth'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.name}>'
    
    @staticmethod
    def get_total_users():
        """Get the total number of registered users"""
        return User.query.count()
    
    @staticmethod
    def get_oauth_users():
        """Get users who registered via OAuth"""
        return User.query.filter_by(registration_method='oauth').all()
    
    @staticmethod
    def get_oauth_users_count():
        """Get count of OAuth users"""
        return User.query.filter_by(registration_method='oauth').count()
