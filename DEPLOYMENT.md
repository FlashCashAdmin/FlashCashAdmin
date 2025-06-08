# FlashCash Production Deployment

## Repository Setup

This repository contains a complete payment platform ready for deployment.

### Quick Deploy to Production

1. **Clone Repository**
```bash
git clone https://github.com/FlashCashAdmin/FlashCashAdmin.git
cd FlashCashAdmin
```

2. **Environment Variables**
Set these in your hosting platform:
```
DATABASE_URL=postgresql://user:pass@host:port/db
STRIPE_SECRET_KEY=sk_live_your_key_here
SENDGRID_API_KEY=SG.your_key_here
SESSION_SECRET=your_secure_session_key
```

3. **Install Dependencies**
```bash
pip install flask flask-sqlalchemy gunicorn psycopg2-binary requests sendgrid sqlalchemy stripe werkzeug email-validator
npm install
npm run build
```

4. **Launch**
```bash
gunicorn --bind 0.0.0.0:$PORT main:app
```

## Platform-Specific Deployment

### Heroku
```bash
git push heroku main
```

### Railway
```bash
railway deploy
```

### DigitalOcean App Platform
- Connect GitHub repository
- Set environment variables
- Deploy automatically

### AWS/GCP/Azure
Use the provided Dockerfile or configure Python runtime with the above commands.

## Features Ready for Production

✅ Stripe payment processing  
✅ Email notifications via SendGrid  
✅ Guest mode transactions  
✅ PostgreSQL database integration  
✅ Mobile-responsive React frontend  
✅ Security hardening  
✅ Error handling and logging  

## Live Demo

Access the test environment at your deployed URL to verify:
- Payment flow at `/test-payment`
- Main application at `/`
- API health at `/api/health` (if implemented)

## Support

Contact the development team for deployment assistance or configuration questions.