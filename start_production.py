#!/usr/bin/env python3
"""
Production server startup script
Automatically detects platform and uses appropriate WSGI server
"""
import os
import sys

def start_production_server():
    """Start the production server with appropriate WSGI server"""
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Starting SmartSEO Analyzer on {host}:{port}")
    print(f"🖥️  Platform: {sys.platform}")
    
    if sys.platform == "win32":
        # Use Waitress for Windows
        print("📦 Using Waitress WSGI server (Windows)")
        from waitress import serve
        from web_app import app
        serve(app, host=host, port=port)
    else:
        # Use Gunicorn for Unix-like systems
        print("📦 Using Gunicorn WSGI server (Unix/Linux)")
        import subprocess
        cmd = [
            'gunicorn',
            '--bind', f'{host}:{port}',
            '--workers', '1',
            '--timeout', '120',
            'web_app:app'
        ]
        subprocess.run(cmd)

if __name__ == '__main__':
    start_production_server()
