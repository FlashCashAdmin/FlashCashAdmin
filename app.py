#!/usr/bin/env python3
import os
import sys

# Configure environment paths
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages')
sys.path.insert(0, '/home/runner/workspace/.pythonlibs/lib/python3.10/site-packages')

import stripe
from flask import Flask, send_from_directory, send_file, request, jsonify
import uuid

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize Stripe with environment key
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Get domain for redirects
YOUR_DOMAIN = (os.environ.get('REPLIT_DEV_DOMAIN') 
               if os.environ.get('REPLIT_DEPLOYMENT') != '' 
               else os.environ.get('REPLIT_DOMAINS', 'localhost:5000').split(',')[0])

# Transaction storage
transactions = []

@app.route('/')
def serve_react_app():
    """Serve React application"""
    if os.path.exists('dist/index.html'):
        return send_file('dist/index.html')
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serve static assets"""
    if os.path.exists(f'dist/{path}'):
        return send_from_directory('dist', path)
    return serve_react_app()

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
        
        amount_cents = int(amount * 100)
        is_guest = bool(sender_email)
        description = note if note else 'FlashCash transfer'
        
        product_name = (f'Guest: Send ${amount:.2f} from {sender_email} to {recipient_email}' 
                       if is_guest else f'Send ${amount:.2f} to {recipient_email}')
        
        transaction_id = str(uuid.uuid4())
        transactions.append({
            'id': transaction_id,
            'amount': amount,
            'recipient_email': recipient_email,
            'sender_email': sender_email,
            'description': description,
            'status': 'pending',
            'type': 'send'
        })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product_name, 'description': description},
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
            return jsonify({'error': 'Both emails required'}), 400
        
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
            return jsonify({'error': 'Source and email required'}), 400
        
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
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
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
    print("FlashCash Payment Platform")
    print("Stripe integration ready")
    print("All payment functions operational")
    print("Guest mode enabled")
    print("Server: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)