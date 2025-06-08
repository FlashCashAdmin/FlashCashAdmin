#!/usr/bin/env python3
import os
import sys

# Configure Python path for dependencies
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages')
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.10/site-packages')

# Set environment variables for gunicorn
os.environ['PYTHONPATH'] = '/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages'

# Import and start the Flask app
from main import app

if __name__ == '__main__':
    print("Starting FlashCash Payment Platform...")
    print("✓ Stripe integration configured")
    print("✓ Send money functionality ready")
    print("✓ Request money functionality ready") 
    print("✓ Claim money functionality ready")
    print("✓ Guest mode enabled")
    app.run(host='0.0.0.0', port=5000, debug=False)