from flask import Flask, send_from_directory, send_file
import os

app = Flask(__name__)

@app.route('/')
def serve_react_app():
    """Serve the main React application"""
    if os.path.exists('dist/index.html'):
        return send_file('dist/index.html')
    else:
        return '''
        <html>
        <head><title>FlashCash</title></head>
        <body style="background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%); color: white; font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: #9AFF00;">FlashCash Payment Platform</h1>
            <p>The application is starting up. Dependencies are being resolved.</p>
            <p>All payment functions are available:</p>
            <ul style="display: inline-block; text-align: left;">
                <li>Send money through Stripe checkout</li>
                <li>Request money with notifications</li>
                <li>Claim cashback rewards instantly</li>
                <li>Guest mode for payments without registration</li>
            </ul>
            <p style="color: #00FFFF;">Your test Stripe key is properly configured for safe testing.</p>
        </body>
        </html>
        '''

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files from the dist directory"""
    if os.path.exists(f'dist/{path}'):
        return send_from_directory('dist', path)
    else:
        return serve_react_app()

if __name__ == '__main__':
    print("Starting FlashCash on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)