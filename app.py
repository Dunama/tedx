from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import os

# Import OAuth components
from src.api.auth.auth import auth_bp, init_oauth
from admin import admin_bp

app = Flask(__name__)
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
        # Remove login logic that references the users dictionary
    return render_template('login.html', form=form)

@app.route('/')
def home():
    return redirect(url_for('auth.signup'))

@app.route('/dashboard')
@login_required
def dashboard():
    return '<h1>Welcome to TEDxYola Dashboard!</h1>'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
