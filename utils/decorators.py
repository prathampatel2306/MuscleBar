from functools import wraps
from flask import session, redirect, url_for, flash
from models.user import User


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        user = User.query.get(session.get("user_id"))

        if not user:
            session.clear()
            flash("Your account is no longer available.", "error")
            return redirect(url_for("auth.login"))

        if "user_id" not in session:



            flash("Please login first.", "error")
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function


def role_required(role):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):


            if session.get("role") != role:

                flash("Unauthorized access.", "error")
                return redirect(url_for("auth.login"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator