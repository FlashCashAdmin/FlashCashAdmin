from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    stripe_customer_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender')
    received_transactions = db.relationship('Transaction', foreign_keys='Transaction.recipient_id', backref='recipient')

class Transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)  # Nullable for requests
    recipient_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)  # Null for requests
    recipient_email = db.Column(db.String(120))  # For sending to non-users
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)  # Optional note
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    transaction_type = db.Column(db.String(20), nullable=False)  # send, request, claim
    stripe_payment_intent_id = db.Column(db.String(100))
    stripe_session_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)