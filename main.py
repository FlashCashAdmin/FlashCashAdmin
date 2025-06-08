#!/usr/bin/env python3
import os
import sys

# Add Python libs to path for Replit environment
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.10/site-packages')
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages')

import stripe
from flask import Flask, send_from_directory, send_file, request, jsonify
from decimal import Decimal
import uuid
import sendgrid
from sendgrid.helpers.mail import Mail

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize Stripe
stripe_key = os.environ.get('STRIPE_SECRET_KEY')
if not stripe_key or stripe_key == 'STRIPE_SECRET_KEY' or not stripe_key.startswith('sk_'):
    print("Warning: Stripe API key not properly configured - needs real secret key starting with 'sk_'")
    stripe_key = None
else:
    print(f"Stripe API key configured: {stripe_key[:12]}...")
stripe.api_key = stripe_key

# Initialize SendGrid
sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

# Get domain for Stripe redirects
YOUR_DOMAIN = (os.environ.get('REPLIT_DEV_DOMAIN') 
               if os.environ.get('REPLIT_DEPLOYMENT') != '' 
               else os.environ.get('REPLIT_DOMAINS', 'localhost:5000').split(',')[0])

# In-memory storage for demo (replace with database in production)
transactions = []

def send_email_notification(to_email, subject, content):
    """Send email notification via SendGrid"""
    try:
        # Use a verified sender email that matches your SendGrid configuration
        from_email = os.environ.get('SENDGRID_FROM_EMAIL', 'crowden071@gmail.com')
        
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )
        response = sg.send(message)
        print(f"Email notification sent to {to_email}: Status {response.status_code}")
        return response.status_code == 202
    except Exception as e:
        print(f"Email notification failed for {to_email}: {e}")
        # Log the notification attempt but don't block the payment flow
        return False

@app.route('/')
def serve_react_app():
    """Serve the main React application"""
    if os.path.exists('dist/index.html'):
        return send_file('dist/index.html')
    else:
        return send_file('index.html')

@app.route('/test-payment')
def test_payment_flow():
    """Serve payment flow test page"""
    return send_file('test_payment_flow.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static files from the dist directory"""
    if os.path.exists(f'dist/{path}'):
        return send_from_directory('dist', path)
    else:
        return serve_react_app()

# API Routes for payment processing
@app.route('/api/create-payment-session', methods=['POST'])
def create_payment_session():
    try:
        # Check if Stripe is properly configured
        if not stripe.api_key or stripe.api_key == 'STRIPE_SECRET_KEY':
            return jsonify({
                'error': 'Payment system not configured. Please contact support.',
                'debug': 'Stripe API key not set'
            }), 503
        
        data = request.get_json()
        amount = float(data.get('amount', 0))
        recipient_email = data.get('recipient_email', '')
        sender_email = data.get('sender_email', '')
        note = data.get('note', '')
        
        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
            
        if not recipient_email:
            return jsonify({'error': 'Recipient email required'}), 400
        
        # Convert to cents for Stripe
        amount_cents = int(amount * 100)
        
        # Determine if this is a guest transaction
        is_guest = bool(sender_email)
        transaction_description = note if note else 'FlashCash transfer'
        
        if is_guest:
            product_name = f'Guest: Send ${amount:.2f} from {sender_email} to {recipient_email}'
        else:
            product_name = f'Send ${amount:.2f} to {recipient_email}'
        
        # Store transaction in memory
        transaction_id = str(uuid.uuid4())
        transactions.append({
            'id': transaction_id,
            'amount': amount,
            'recipient_email': recipient_email,
            'sender_email': sender_email,
            'description': transaction_description,
            'status': 'pending',
            'type': 'send'
        })

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product_name,
                        'description': transaction_description
                    },
                    'unit_amount': amount_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'https://{YOUR_DOMAIN}/?payment=success&session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'https://{YOUR_DOMAIN}/?payment=cancelled',
            metadata={
                'amount': str(amount),
                'recipient_email': recipient_email,
                'sender_email': sender_email if is_guest else '',
                'note': note,
                'transaction_id': transaction_id
            }
        )
        
        return jsonify({
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/request-money', methods=['POST'])
def request_money():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_email = data.get('from_email', '')
        requester_email = data.get('requester_email', '')
        description = data.get('description', '')
        
        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
            
        if not from_email or not requester_email:
            return jsonify({'error': 'Both requester and recipient emails required'}), 400
        
        # Store request in memory
        transaction_id = str(uuid.uuid4())
        transactions.append({
            'id': transaction_id,
            'amount': amount,
            'from_email': from_email,
            'requester_email': requester_email,
            'description': description or f'Money request from {requester_email}',
            'status': 'pending',
            'type': 'request'
        })
        
        # Send email notification
        email_subject = f"FlashCash: Money Request for ${amount:.2f}"
        email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #000; color: #fff; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; border-radius: 10px;">
                <h2 style="color: #9AFF00; margin-bottom: 20px;">Money Request Received</h2>
                <p style="font-size: 16px; line-height: 1.6;">
                    <strong>{requester_email}</strong> has requested <strong style="color: #00FFFF;">${amount:.2f}</strong> from you.
                </p>
                {f'<p style="color: #ccc; margin: 15px 0;"><em>Message: {description}</em></p>' if description else ''}
                <div style="margin: 30px 0;">
                    <a href="https://{YOUR_DOMAIN}" style="background: #9AFF00; color: #000; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Pay Request on FlashCash
                    </a>
                </div>
                <p style="color: #888; font-size: 14px;">
                    Secure payments powered by FlashCash
                </p>
            </div>
        </body>
        </html>
        """
        
        send_email_notification(from_email, email_subject, email_content)
        
        return jsonify({
            'status': 'success',
            'message': f'Money request of ${amount:.2f} sent to {from_email}',
            'transaction_id': transaction_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/claim-money', methods=['POST'])
def claim_money():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        source = data.get('source', '')
        claimer_email = data.get('claimer_email', '')
        
        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400
            
        if not source or not claimer_email:
            return jsonify({'error': 'Source and claimer email required'}), 400
        
        # Store claim in memory
        transaction_id = str(uuid.uuid4())
        transactions.append({
            'id': transaction_id,
            'amount': amount,
            'claimer_email': claimer_email,
            'source': source,
            'description': f'Cashback claim from {source}',
            'status': 'completed',
            'type': 'claim'
        })
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully claimed ${amount:.2f} from {source}',
            'transaction_id': transaction_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment-success')
def payment_success():
    session_id = request.args.get('session_id')
    if session_id:
        try:
            # Retrieve the session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                # Update transaction status in memory
                transaction_id = session.metadata.get('transaction_id')
                if transaction_id:
                    for tx in transactions:
                        if tx['id'] == transaction_id:
                            tx['status'] = 'completed'
                            break
                
                # Send payment confirmation email
                recipient_email = session.metadata.get('recipient_email')
                sender_email = session.metadata.get('sender_email')
                amount = session.metadata.get('amount')
                
                if recipient_email:
                    email_subject = f"FlashCash: Payment Received - ${amount}"
                    email_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; background: #000; color: #fff; padding: 20px;">
                        <div style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; border-radius: 10px;">
                            <h2 style="color: #9AFF00; margin-bottom: 20px;">Payment Received!</h2>
                            <p style="font-size: 16px; line-height: 1.6;">
                                You have received <strong style="color: #00FFFF;">${amount}</strong> 
                                {f'from {sender_email}' if sender_email else 'via FlashCash'}.
                            </p>
                            <div style="margin: 30px 0; padding: 20px; background: rgba(154, 255, 0, 0.1); border-radius: 5px;">
                                <p style="color: #9AFF00; font-weight: bold; margin: 0;">
                                    ✓ Payment processed successfully
                                </p>
                            </div>
                            <div style="margin: 30px 0;">
                                <a href="https://{YOUR_DOMAIN}" style="background: #9AFF00; color: #000; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                                    View on FlashCash
                                </a>
                            </div>
                            <p style="color: #888; font-size: 14px;">
                                Secure payments powered by FlashCash
                            </p>
                        </div>
                    </body>
                    </html>
                    """
                    send_email_notification(recipient_email, email_subject, email_content)
                
                return jsonify({
                    'status': 'success',
                    'message': 'Payment completed successfully'
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid session'}), 400

# WSGI entry point for gunicorn
application = app

if __name__ == '__main__':
    print("Starting FlashCash Payment Platform...")
    print("✓ Stripe integration configured")
    print("✓ Send money functionality ready")
    print("✓ Request money functionality ready") 
    print("✓ Claim money functionality ready")
    print("✓ Guest mode enabled")
    print("Server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)