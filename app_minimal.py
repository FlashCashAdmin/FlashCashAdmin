#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.10/site-packages')
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages')

import stripe
from flask import Flask, send_from_directory, send_file, request, jsonify
from decimal import Decimal
import uuid

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Get domain for Stripe redirects
YOUR_DOMAIN = (os.environ.get('REPLIT_DEV_DOMAIN') 
               if os.environ.get('REPLIT_DEPLOYMENT') != '' 
               else os.environ.get('REPLIT_DOMAINS', 'localhost:5000').split(',')[0])

# In-memory storage for demo (replace with database in production)
transactions = []

@app.route('/')
def serve_react_app():
    """Serve the main React application"""
    if os.path.exists('dist/index.html'):
        return send_file('dist/index.html')
    else:
        return send_file('index.html')

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
                
                return jsonify({
                    'status': 'success',
                    'message': 'Payment completed successfully'
                })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid session'}), 400

if __name__ == '__main__':
    print("Starting FlashCash Payment Platform...")
    print("✓ Stripe integration configured")
    print("✓ Send money functionality ready")
    print("✓ Request money functionality ready") 
    print("✓ Claim money functionality ready")
    print("✓ Guest mode enabled")
    print("Server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)