from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from authlib.integrations.flask_client import OAuth
from src.models import db, User
from src.form import SignupForm, LoginForm
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
            user = User(name=username, email=email, password=password)
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
    Show login form and validate dummy credentials
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # You can replace this with real user DB lookup
        user = User.query.filter_by(name=username).first()
        if user:
            session["user"] = {"name": user.name, "email": user.email}
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html", form=form)




auth_bp = Blueprint("auth", __name__)
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name="myApp",
        client_id=os.getenv("OAUTH2_CLIENT_ID"),
        client_secret=os.getenv("OAUTH2_CLIENT_SECRET"),
        server_metadata_url=os.getenv("OAUTH2_METADATA_URL"),
        client_kwargs={"scope": "openid email profile"},
    )

@auth_bp.route("/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            user = User(name=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

        session["user"] = {"name": username, "email": email}
        flash("Account created successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("signup.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(name=username).first()
        if user and (user.password == password):
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

        if not User.query.filter_by(email=email).first():
            new_user = User(email=email, name=name)
            db.session.add(new_user)
            db.session.commit()

        flash(f"Welcome, {name}!", "success")
        return redirect(url_for("dashboard"))

    except Exception as e:
        print(f"[Google OAuth Error]: {e}")
        flash("Google Sign-In failed.", "error")
        return redirect(url_for("auth.signup"))
