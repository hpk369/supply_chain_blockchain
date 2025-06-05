from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# In-memmory user store. In production use a DB instead.
USERS = {
  # Pre-created admin
  "admin1": {
    "password_hash": generate_password_hash("adminpass"),
    "role": "admin"
  },
  # Two example users
  "userA": {
    "password_hash": generate_password_hash("userApass"),
    "role": "user"
  },
  "UserB": {
    "password_hash": generate_password_hash("userBpass"),
    "role": "user"
  }
}

class User(UserMixin):
  '''
  A simple User class that Flask-Login can work with.
  user.id == username
  '''

  def __init__(self, username: str, role: str):
    self.id = username
    self.role = role

  @staticmethod
  def get(username: str):
    # Given a username, return a User instance if it exists in USERS, or None otherwise
    info = USERS.get(username)
    if info is None:
      return None
    return User(username, info["role"])
  
  @staticmethod
  def validate_credentials(username: str, password: str) -> bool:
    # Check if a given username/password combination is valid
    user_record = USERS.get(username)
    if not user_record:
      return False
    return check_password_hash(user_record["password_hash"], password)