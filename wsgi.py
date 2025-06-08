#!/usr/bin/env python3
import os
import sys

# Configure Python path for Replit environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.pythonlibs', 'lib', 'python3.11', 'site-packages'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.pythonlibs', 'lib', 'python3.10', 'site-packages'))

# Import the Flask application
from main import app

# WSGI application entry point
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)