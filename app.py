from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os

# Import OAuth components
from src.api.auth.auth import auth_bp, init_oauth
from admin import admin_bp
from src.api.auth.dummy_db import dummy_db

app = Flask(__name__, static_folder='src/static', template_folder='src/templates')
app.secret_key = os.urandom(24)

# Register the auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

# Register the admin blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

# Initialize OAuth
init_oauth(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Dummy authentication: accept any username/password
        if username and password:
            session['user'] = {'name': username}
            return redirect(url_for('dashboard'))  # <-- Fix: use 'dashboard' not 'userDashboard'
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/')
def home():
    return redirect(url_for('auth.signup'))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('userDashboard.html', user=user)

@app.route('/admin/users')
def admin_users():
    token = request.args.get('token')
    if token != os.getenv('ADMIN_TOKEN'):
        flash('Admin access required. Invalid or missing token.', 'error')
        # Redirect to the admin page, not the login page
        return redirect(url_for('admin_users', token=os.getenv('ADMIN_TOKEN')))
    # Gather stats from dummy_db
    total_users = len(getattr(dummy_db, 'users', []))
    checked_in = 0  # Placeholder: replace with real checked-in logic if available
    event_capacity = 300
    checkin_rate = f"{(checked_in / total_users * 100) if total_users else 0:.0f}%"
    return render_template(
        'admin.html',
        total_users=total_users,
        checked_in=checked_in,
        event_capacity=event_capacity,
        checkin_rate=checkin_rate
    )

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
