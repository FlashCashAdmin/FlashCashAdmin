FROM python:3.11-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY pyproject.toml ./

# Install dependencies
RUN npm install
RUN pip install flask flask-sqlalchemy gunicorn psycopg2-binary requests sendgrid sqlalchemy stripe werkzeug email-validator

# Copy source code
COPY . .

# Build frontend
RUN npm run build

# Expose port
EXPOSE 5000

# Start command
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]