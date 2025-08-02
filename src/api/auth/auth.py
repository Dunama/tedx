from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from authlib.integrations.flask_client import OAuth
from src.models import db, User
from src.form import SignupForm, LoginForm
from datetime import datetime
import os

auth_bp = Blueprint("auth", __name__)
oauth = OAuth()


# -------------------- OAuth Initialization --------------------
def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="myApp",
        client_id=os.getenv("OAUTH2_CLIENT_ID"),
        client_secret=os.getenv("OAUTH2_CLIENT_SECRET"),
        server_metadata_url=os.getenv("OAUTH2_METADATA_URL"),
        client_kwargs={"scope": "openid email profile"},
    )


# -------------------- Signup --------------------
@auth_bp.route("/", methods=["GET", "POST"])
def signup():
    """
    Show signup form and handle form submission
    """
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data  # NOTE: Not hashed (not secure for production)

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            user = User(
                name=username, 
                email=email, 
                password=password,
                registration_method='local'
            )
            db.session.add(user)
            db.session.commit()

        session["user"] = {"name": username, "email": email}
        flash("Account created successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("signup.html", form=form)


# -------------------- Login --------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Show login form and validate credentials
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Look up user in database
        user = User.query.filter_by(name=username).first()
        if user and (user.password == password):
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            session["user"] = {"name": user.name, "email": user.email}
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html", form=form)


@auth_bp.route("/googleLogin")
def googleLogin():
    try:
        redirect_uri = url_for("auth.googleCallback", _external=True)
        return oauth.myApp.authorize_redirect(redirect_uri)
    except Exception as e:
        flash("Error initiating Google login.", "error")
        return redirect(url_for("auth.signup"))


@auth_bp.route("/signin-google")
def googleCallback():
    try:
        token = oauth.myApp.authorize_access_token()
        user_info = token.get("userinfo")

        if not user_info or not user_info.get("email"):
            flash("Failed to retrieve email from Google.", "error")
            return redirect(url_for("auth.signup"))

        email = user_info["email"]
        name = user_info.get("name", "Guest")

        session["user"] = {"email": email, "name": name, "userinfo": user_info}

        # Check if user exists, if not create new OAuth user
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(
                email=email, 
                name=name,
                registration_method='oauth'
            )
            db.session.add(new_user)
            db.session.commit()
        else:
            # Update last login time for existing user
            existing_user.last_login = datetime.utcnow()
            db.session.commit()

        flash(f"Welcome, {name}!", "success")
        return redirect(url_for("dashboard"))

    except Exception as e:
        print(f"[Google OAuth Error]: {e}")
        flash("Google Sign-In failed.", "error")
        return redirect(url_for("auth.signup"))
