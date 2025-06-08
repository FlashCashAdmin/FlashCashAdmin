# FlashCash Payment Functions - End-to-End Process

## 1. Guest Send Money (No Login Required)

### User Journey:
1. **Landing Page Access**
   - User visits FlashCash landing page
   - Clicks "Send Money as Guest" button (electric green with neon styling)

2. **Guest Send Money Modal**
   - Modal opens with form fields:
     - Your Email (required) - sender identification
     - Amount ($) (required) - minimum $0.01
     - Send To (required) - recipient email
     - Note (optional) - transaction description
   - User fills in required fields
   - Clicks "Send Money" button

3. **Stripe Payment Processing**
   - Frontend sends POST to `/api/create-payment-session`
   - Backend creates Stripe checkout session with:
     - Product name: "Guest: Send $X.XX from sender@email.com to recipient@email.com"
     - Description: User's note or "FlashCash transfer"
     - Metadata includes: sender_email, recipient_email, amount, note, is_guest=true
   - User redirected to Stripe hosted checkout page

4. **Payment Completion**
   - User completes payment on Stripe
   - Success: Redirected to `/?payment=success&session_id=XXX`
   - Cancel: Redirected to `/?payment=cancelled`
   - Backend can retrieve session details via Stripe API for transaction logging

## 2. Authenticated User Send Money

### User Journey:
1. **Dashboard Access**
   - User logs in through login page
   - Navigates to Dashboard (Home tab active by default)

2. **Send Money Action**
   - User clicks "Send" button on home tab
   - Send Money modal opens with form:
     - Amount (required)
     - To (required) - recipient name or email
     - Note (optional) - what's this for
   - User submits form

3. **Stripe Payment Processing**
   - Similar to guest mode but without sender_email field
   - Product name: "Send $X.XX to recipient"
   - User redirected to Stripe checkout
   - Success/cancel redirects handle authenticated state

4. **Transaction Recording**
   - Payment creates transaction record in database
   - Notification added to user's notification feed
   - Transaction appears in Activity tab history

## 3. Request Money Function

### User Journey:
1. **Dashboard Request**
   - Authenticated user on dashboard
   - Clicks "Request" button
   - Request Money modal opens

2. **Request Form**
   - Amount (required)
   - From (required) - who to request from
   - Description (optional) - reason for request
   - Submit creates pending transaction

3. **Request Processing**
   - Creates transaction with type: 'request'
   - Status: 'pending'
   - Adds notification to user feed
   - In real implementation, would send email/notification to requested party

## 4. Claim Money Function

### User Journey:
1. **Dashboard Claim**
   - User clicks "Claim" button
   - Claim Money modal opens

2. **Claim Form**
   - Amount (required)
   - Source (required) - where to claim from
   - Submit processes claim

3. **Claim Processing**
   - Creates transaction with type: 'claim'
   - Status: 'approved' (immediate for demo)
   - Adds success notification
   - Updates user's transaction history

## Technical Implementation Details

### API Endpoints:
- `POST /api/create-payment-session` - Creates Stripe checkout for send money
- `GET /api/payment-success` - Handles payment completion callbacks

### Database Models:
- User: id, username, email, balance, stripe_customer_id
- Transaction: id, sender_id, recipient_id, amount, description, status, type, stripe_session_id

### Stripe Integration:
- Uses Stripe Checkout Sessions for secure payment processing
- Supports both guest and authenticated transactions
- Metadata tracks transaction details for reconciliation
- Success/cancel URLs handle post-payment flow

### Security Features:
- All amounts validated server-side
- Email validation for guest mode
- Stripe handles all sensitive payment data
- HTTPS required for production deployment

### User Experience:
- Optional note fields reduce friction
- Guest mode eliminates registration barrier
- Real-time notifications for transaction updates
- Mobile-responsive neon design throughout