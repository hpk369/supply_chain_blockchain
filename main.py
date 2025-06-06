from app import create_app

app = create_app()

if __name__ == "__main__":
  # debug-True for local development; remove in production
  app.run(host="0.0.0.0", port=9567, debug=True)