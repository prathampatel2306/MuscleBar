from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from models.user import User
from database import db

auth = Blueprint("auth", __name__)

ADMIN_SECRET_CODE = "MUSCLEBAR@2026"
# ===========================
# SIGNUP
# ===========================
@auth.route("/", methods=["GET", "POST"])
def signup():

    ADMIN_SECRET_CODE = "MUSCLEBAR@2026"

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm-password", "")
        role = request.form.get("role", "")
        admin_code = request.form.get("admin_code", "").strip()

        # Empty fields
        if not username or not password or not role:
            flash("Please fill all fields.", "error")
            return redirect(url_for("auth.signup"))

        # Password Match
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("auth.signup"))

        # Admin Secret Code Validation
        if role == "admin":
            if admin_code != ADMIN_SECRET_CODE:
                flash("Invalid Admin Secret Code.", "error")
                return redirect(url_for("auth.signup"))

        # Username Exists
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.", "error")
            return redirect(url_for("auth.signup"))

        # Create User
        new_user = User(
            username=username,
            role=role
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully.", "success")

        return redirect(url_for("auth.login"))

    return render_template("signup.html")

# ===========================
# LOGIN
# ===========================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Invalid username.", "error")
            return redirect(url_for("auth.login"))

        if user.role != role:
            flash("Incorrect role selected.", "error")
            return redirect(url_for("auth.login"))

        if not user.check_password(password):
            flash("Incorrect password.", "error")
            return redirect(url_for("auth.login"))

        # Create session
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        session["profile_completed"] = user.profile_completed

        # Redirect according to role
        if user.role == "member":

            if user.profile_completed:
                return redirect(url_for("member.member_dashboard"))

            return redirect(url_for("member.plan"))

        elif user.role == "trainer":

            if user.profile_completed:
                return redirect(url_for("trainer.trainer_dashboard"))

            return redirect(url_for("trainer.trainer_profile"))

        else:

            return redirect(url_for("admin.admin_landing"))

    return render_template("login.html")


# ===========================
# LOGOUT
# ===========================

@auth.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))