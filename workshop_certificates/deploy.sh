#!/bin/bash

# Production Deployment Script for Workshop Certificates App
# Usage: ./deploy.sh [environment]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default environment
ENVIRONMENT=${1:-production}

echo -e "${BLUE}🚀 Starting deployment for environment: ${ENVIRONMENT}${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

if ! command_exists docker; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

if ! command_exists docker-compose; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cat > .env << EOF
# Database Configuration
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://workshop_user:your_secure_password_here@db:5432/workshop_certificates

# Flask Configuration
SECRET_KEY=your_super_secret_key_here_change_this_in_production
FLASK_ENV=production
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Application Configuration
PORT=8000
HOST=0.0.0.0
EOF
    echo -e "${GREEN}✅ .env file created. Please update the passwords and secret key!${NC}"
fi

# Create SSL directory and self-signed certificate for development
if [ ! -d ssl ]; then
    echo -e "${YELLOW}🔐 Creating SSL directory and self-signed certificate...${NC}"
    mkdir -p ssl
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    echo -e "${GREEN}✅ SSL certificate created${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}📁 Creating necessary directories...${NC}"
mkdir -p uploads certificates logs
echo -e "${GREEN}✅ Directories created${NC}"

# Build and start services
echo -e "${YELLOW}🔨 Building and starting services...${NC}"

if [ "$ENVIRONMENT" = "production" ]; then
    # Production deployment with nginx
    docker-compose --profile production up -d --build
else
    # Development deployment without nginx
    docker-compose up -d --build
fi

echo -e "${GREEN}✅ Services started${NC}"

# Wait for services to be healthy
echo -e "${YELLOW}⏳ Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
echo -e "${YELLOW}🏥 Checking service health...${NC}"

# Check database
if docker-compose exec -T db pg_isready -U workshop_user -d workshop_certificates > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Database is healthy${NC}"
else
    echo -e "${RED}❌ Database health check failed${NC}"
    exit 1
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis is healthy${NC}"
else
    echo -e "${RED}❌ Redis health check failed${NC}"
    exit 1
fi

# Check application
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application is healthy${NC}"
else
    echo -e "${RED}❌ Application health check failed${NC}"
    echo -e "${YELLOW}⏳ Waiting a bit more for application to start...${NC}"
    sleep 20
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application is now healthy${NC}"
    else
        echo -e "${RED}❌ Application health check still failed${NC}"
        echo -e "${YELLOW}📋 Checking application logs...${NC}"
        docker-compose logs app
        exit 1
    fi
fi

# Show service status
echo -e "${YELLOW}📊 Service status:${NC}"
docker-compose ps

# Show application info
echo -e "${BLUE}🌐 Application URLs:${NC}"
echo -e "${GREEN}   HTTP:  http://localhost${NC}"
if [ "$ENVIRONMENT" = "production" ]; then
    echo -e "${GREEN}   HTTPS: https://localhost${NC}"
fi
echo -e "${GREEN}   Health: http://localhost:8000/health${NC}"
echo -e "${GREEN}   Admin:  http://localhost:8000/admin${NC}"

# Show logs
echo -e "${BLUE}📋 Recent application logs:${NC}"
docker-compose logs --tail=20 app

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${YELLOW}💡 Don't forget to:${NC}"
echo -e "${YELLOW}   1. Update passwords in .env file${NC}"
echo -e "${YELLOW}   2. Set up proper SSL certificates for production${NC}"
echo -e "${YELLOW}   3. Configure your domain name${NC}"
echo -e "${YELLOW}   4. Set up monitoring and backups${NC}"

# Useful commands
echo -e "${BLUE}🔧 Useful commands:${NC}"
echo -e "${GREEN}   View logs:     docker-compose logs -f app${NC}"
echo -e "${GREEN}   Stop services: docker-compose down${NC}"
echo -e "${GREEN}   Restart app:   docker-compose restart app${NC}"
echo -e "${GREEN}   Update app:    docker-compose up -d --build app${NC}" 