from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from .models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  '''
  Show login form and process login submissions.
  If credentials are valid, logs in user and redirects to correct dashboard.
  '''
  if current_user.is_authenticated:
    # If already logged in, redirect to appropriate dashboard
    if current_user.role == "admin":
      return redirect(url_for("admin.admin_dashboard"))
    else:
      return redirect(url_for("user.user_dashboard"))
    
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    if User.validate_credentials(username, password):
      user = User.get(username)
      login_user(user)
      # Redirect to role-specific dashboard
      if user.role == "admin":
        return redirect(url_for("admin.admin_dashboard"))
      else:
        return redirect(url_for("user.user_dashboard"))
    else:
      flash("Invalid username or password", "danger")
      return redirect(url_for("auth.login"))
    
  # GET request: render login form
  return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
  # Logout of current user and redirect to login page
  logout_user()
  return redirect(url_for("auth.login"))
    