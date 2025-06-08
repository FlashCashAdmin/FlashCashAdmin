# FlashCash - Modern Payment Platform

FlashCash is a comprehensive payment request platform that simplifies financial interactions through intuitive design and smart technology.

## Features

- **Modern React Frontend** - Responsive mobile-first interface with neon styling
- **Secure Payment Processing** - Stripe integration for seamless transactions
- **Guest Mode Support** - Send money without requiring account registration
- **Email Notifications** - SendGrid integration for transaction confirmations
- **Real-time Updates** - Interactive UI with transaction tracking
- **PostgreSQL Database** - Reliable data storage and transaction history

## Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: Flask, Python 3.11
- **Database**: PostgreSQL with SQLAlchemy
- **Payment**: Stripe Checkout
- **Email**: SendGrid
- **Deployment**: Gunicorn WSGI server

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL
- Stripe account
- SendGrid account

### Environment Setup

Create environment variables:

```bash
DATABASE_URL=postgresql://username:password@host:port/database
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
SENDGRID_API_KEY=SG.your_sendgrid_api_key
SESSION_SECRET=your_session_secret
```

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Build the frontend:
```bash
npm run build
```

4. Initialize the database:
```bash
python -c "from main import db; db.create_all()"
```

### Running the Application

Start the server:
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

Access the application at `http://localhost:5000`

## API Endpoints

### Payment Operations

- `POST /api/create-payment-session` - Create Stripe checkout session
- `POST /api/request-money` - Send money request via email
- `POST /api/claim-money` - Process money claim
- `GET /payment-success` - Handle successful payments

### Testing

Access the payment flow test page at `/test-payment` to verify Stripe integration.

## Project Structure

```
FlashCash/
├── src/                    # React frontend source
│   ├── components/         # Reusable UI components
│   ├── pages/             # Application pages
│   └── utils/             # Utility functions
├── main.py                # Flask application entry point
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
└── dist/                  # Built frontend assets
```

## Design Philosophy

FlashCash uses a strict neon aesthetic with electric green (#9AFF00) and cyan (#00FFFF) accents, featuring:

- Abstract line icons
- Window-fitting condensed layout
- Three-tab organization (Home, Activity, Profile)
- Mobile-first responsive design

## Security

- Secure Stripe payment processing
- Environment variable configuration
- CSRF protection
- Input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For issues and questions, contact the FlashCash team or create an issue in this repository.