"""
WSGI entry point for production deployment
"""
from web_app import app

if __name__ == "__main__":
    app.run()
