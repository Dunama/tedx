from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from src.models import db  # Your SQLAlchemy models
from src.api.auth.auth import auth_bp, init_oauth
from admin import admin_bp
import os

# -------------------- Flask App Setup --------------------

app = Flask(__name__, static_folder='src/static', template_folder='src/templates')

# Secret key (should be set securely in .env or Render environment)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# Database config (Render will use DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tedx.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# OAuth2 Setup
init_oauth(app)

# -------------------- Flask-Login --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return None  # Optional: integrate real User model later

# -------------------- Login Form --------------------

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# -------------------- Routes --------------------

@app.route('/')
def home():
    return redirect(url_for('auth.signup'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instantiate the form outside the POST block

    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            # Dummy login logic (replace with real DB authentication)
            if username and password:
                session['user'] = {'name': username}
                flash('Logged in successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
      
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))

@app.route('/admin/users')
def admin_users():
    from src.api.auth.dummy_db import dummy_db  # imported here to avoid circular import errors
    token = request.args.get('token')
    expected_token = os.getenv('ADMIN_TOKEN')

    if token != expected_token:
        flash('Admin access required. Invalid or missing token.', 'error')
        return redirect(url_for('admin_users', token=expected_token))

    total_users = len(getattr(dummy_db, 'users', []))
    checked_in = 0
    event_capacity = 300
    checkin_rate = f"{(checked_in / total_users * 100) if total_users else 0:.0f}%"

    return render_template(
        'admin.html',
        total_users=total_users,
        checked_in=checked_in,
        event_capacity=event_capacity,
        checkin_rate=checkin_rate
    )

# -------------------- Blueprints --------------------

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

# -------------------- Run App --------------------

if __name__ == '__main__':
    app.run(debug=True)
