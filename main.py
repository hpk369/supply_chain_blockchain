from app import create_app

from flask import redirect, url_for

app = create_app()

@app.route("/")
def index():
  # send everyone to the login page
  return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(port=9567, ssl_context=('localhost+1.pem','localhost+1-key.pem'))
