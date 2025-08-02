from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from src.models import db
from src.api.auth.auth import auth_bp, init_oauth
from admin import admin_bp
import os

# Import all models so they're registered with SQLAlchemy
from src.db.models.events import Event

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
# csrf = CSRFProtect(app)  # Temporarily disabled for API testing

# Exempt API endpoints from CSRF protection
# csrf.exempt('src.api.registration_desk.registration_bp')

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
    token = request.args.get('token')
    expected_token = os.getenv('ADMIN_TOKEN')

    if token != expected_token:
        flash('Admin access required. Invalid or missing token.', 'error')
        return redirect(url_for('admin_users', token=expected_token))

    return render_template('admin.html')

# -------------------- Database Initialization --------------------

def create_tables():
    """Create database tables and populate with sample data"""
    db.create_all()
    
    # Import and populate attendee data
    from src.db.models.events import Event, attendees
    
    # Check if data already exists
    try:
        if Event.query.count() == 0:
            for attendee in attendees:
                event = Event(
                    event_id=attendee['event_id'],
                    name=attendee['name'],
                    email=attendee['email'],
                    location=attendee['Location']
                )
                db.session.add(event)
            db.session.commit()
            print(f"Database populated with {len(attendees)} attendees")
    except Exception as e:
        # If table doesn't exist yet, skip population for now
        print(f"Database initialization will be done after migration: {e}")

# Database initialization will be done via migrations
# Uncomment the following lines if you want to initialize without migrations:
# with app.app_context():
#     create_tables()

# -------------------- Blueprints --------------------

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

from src.api.registration_desk import registration_bp
app.register_blueprint(registration_bp, url_prefix='/registration')

# -------------------- Run App --------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Populate initial data if needed
        from src.db.models.events import Event, attendees
        if Event.query.count() == 0:
            try:
                for attendee in attendees:
                    event = Event(
                        event_id=attendee['event_id'],
                        name=attendee['name'],
                        email=attendee['email'],
                        location=attendee['Location']
                    )
                    db.session.add(event)
                db.session.commit()
                print(f"Database populated with {len(attendees)} attendees")
            except Exception as e:
                db.session.rollback()
                print(f"Error populating database: {e}")
    
    app.run(debug=True)
