#!/usr/bin/env python3
import os
import sys
sys.path.append('/opt/virtualenvs/python3/lib/python3.11/site-packages')
import stripe

# Debug Stripe configuration
print("=== Stripe Debug Info ===")
stripe_key = os.environ.get('STRIPE_SECRET_KEY')
print(f"Raw env var: {repr(stripe_key)}")
print(f"Key length: {len(stripe_key) if stripe_key else 0}")
print(f"Starts with sk_: {stripe_key.startswith('sk_') if stripe_key else False}")

if stripe_key and stripe_key != 'STRIPE_SECRET_KEY' and stripe_key.startswith('sk_'):
    stripe.api_key = stripe_key
    try:
        # Test API connection
        account = stripe.Account.retrieve()
        print(f"✓ Stripe connected successfully")
        print(f"Account ID: {account.id}")
    except Exception as e:
        print(f"✗ Stripe error: {e}")
else:
    print("✗ Invalid or missing Stripe key")