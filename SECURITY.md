# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Features

### Data Protection
- All sensitive data stored as environment variables
- No hardcoded API keys or credentials
- PostgreSQL database encryption at rest
- Secure session management with Flask

### Payment Security
- Stripe PCI DSS Level 1 compliance
- No credit card data stored locally
- Secure checkout flow via Stripe hosted pages
- Webhook signature verification

### API Security
- Input validation on all endpoints
- CSRF protection enabled
- Rate limiting recommended for production
- SQL injection prevention via SQLAlchemy ORM

### Environment Security
- Production environment variable validation
- Secure random session key generation
- Database connection pooling with SSL
- HTTPS enforcement in production

## Reporting a Vulnerability

To report a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. Email security concerns to the development team
3. Include detailed description of the vulnerability
4. Provide steps to reproduce if applicable
5. Allow 48 hours for initial response

## Security Checklist for Deployment

### Before Production
- [ ] All environment variables properly configured
- [ ] Stripe webhooks enabled with signature verification
- [ ] HTTPS certificate installed and configured
- [ ] Database connection secured with SSL
- [ ] SendGrid sender domain verified
- [ ] Rate limiting configured
- [ ] Error logging configured without exposing sensitive data
- [ ] Regular security updates scheduled

### Ongoing Security
- [ ] Monitor Stripe dashboard for suspicious activity
- [ ] Review access logs regularly
- [ ] Keep dependencies updated
- [ ] Backup database regularly
- [ ] Monitor error rates and unusual patterns

## Dependencies Security

This project uses the following security-critical dependencies:

- **Stripe Python Library**: Regularly updated for security patches
- **Flask**: Secure configuration with CSRF protection
- **SQLAlchemy**: Parameterized queries prevent SQL injection
- **psycopg2**: Secure PostgreSQL adapter
- **SendGrid**: Authenticated email delivery

## Contact

For security-related questions or concerns, contact the FlashCash security team.