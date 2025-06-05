from flask import Flask
from flask_login import LoginManager

from .models import User

login_manager = LoginManager()
login_manager.login_view = "auth.login" # Redirect to 'auth.login' if not authenticated

def create_app():
  app = Flask(__name__)
  app.config["SECRET_KEY"] = "replace-this-with-a-random-secret"  # Change in production

  # Initialize the Flask-login
  login_manager.init_app(app)

  # User loader callback
  @login_manager.user_loader
  def load_user(user_id):
    '''
    Given a user_id (str), return a User object or None
    We stored users in-memory in app.models.USERS, keyed by username
    '''
    return User.get(user_id)  # Returns None if not found
  
  # Import and register blueprints
  from .auth import auth_bp
  from .admin.routes import admin_bp
  from .user.routes import user_bp

  app.register_blueprint(auth_bp)
  app.register_blueprint(admin_bp)
  app.register_blueprint(user_bp)

  return app