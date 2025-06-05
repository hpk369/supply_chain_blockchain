from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
  '''
  Decorator to ensure current_user.role is in the provided roles.
  Usage:
    @roles_required("admin")
    def some_admin_route(): ...
  '''

  def decorator(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
      if not current_user.is_authenticated:
        # Let Flask-Login redirect to login page
        return abort(401)
      if current_user.role not in roles:
        return abort(403)
      return f(*args, **kwargs)
    return wrapped
  return decorator