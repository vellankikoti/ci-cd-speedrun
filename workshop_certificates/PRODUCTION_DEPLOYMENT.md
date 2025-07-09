# Production Deployment Guide

This guide covers deploying the Workshop Certificates Flask application to production using Docker and Docker Compose.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Domain name (for production)
- SSL certificates (for HTTPS)

### 1. Clone and Setup

```bash
git clone <your-repo>
cd workshop_certificates
```

### 2. Configure Environment

Edit the `.env` file with your production settings:

```bash
# Database Configuration
POSTGRES_PASSWORD=your_secure_production_password
DATABASE_URL=postgresql://workshop_user:your_secure_production_password@db:5432/workshop_certificates

# Flask Configuration
SECRET_KEY=your_super_secret_production_key_here
FLASK_ENV=production
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Application Configuration
PORT=8000
HOST=0.0.0.0
```

### 3. Deploy

```bash
# Development deployment (without nginx)
./deploy.sh development

# Production deployment (with nginx and SSL)
./deploy.sh production
```

## 📋 Architecture

The application uses a multi-service architecture:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │   Redis     │    │ PostgreSQL  │
│  (Proxy)    │    │  (Cache)    │    │ (Database)  │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌─────────────┐
                    │   Flask     │
                    │  (App)      │
                    └─────────────┘
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_PASSWORD` | Database password | `workshop_password` |
| `SECRET_KEY` | Flask secret key | `dev-secret` |
| `FLASK_ENV` | Flask environment | `production` |
| `UPLOAD_FOLDER` | Upload directory | `uploads` |
| `MAX_CONTENT_LENGTH` | Max upload size | `16777216` (16MB) |

### Database Configuration

The application supports both SQLite (development) and PostgreSQL (production):

- **Development**: Uses SQLite database file
- **Production**: Uses PostgreSQL with connection pooling

### SSL Configuration

For production, you need SSL certificates:

1. **Self-signed** (development): Automatically created by deploy script
2. **Let's Encrypt** (production): Use certbot or similar
3. **Commercial certificates**: Place in `ssl/` directory

## 🏥 Health Checks

The application includes comprehensive health checks:

### Application Health

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": 1234567890.123,
  "uptime_hours": 2.5,
  "version": "1.0.0",
  "database": "healthy",
  "system": {
    "memory_usage_percent": 45.2,
    "cpu_usage_percent": 12.8,
    "memory_available_mb": 2048.5
  }
}
```

### Docker Health Checks

- **Database**: `pg_isready` check every 10s
- **Redis**: `ping` check every 10s
- **Application**: HTTP health check every 30s

## 📊 Monitoring

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f nginx
```

### Metrics

The health endpoint provides basic metrics:
- Memory usage
- CPU usage
- Uptime
- Database connectivity

### Alerts

Set up monitoring for:
- Health check failures
- High memory usage (>80%)
- High CPU usage (>80%)
- Database connection errors

## 🔒 Security

### Security Headers

Nginx includes security headers:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

### Rate Limiting

- **Login endpoints**: 5 requests/minute
- **API endpoints**: 10 requests/second
- **Burst allowance**: 10-20 requests

### File Upload Security

- Maximum file size: 16MB
- Allowed formats: PNG, JPG, JPEG, GIF
- Files stored outside web root
- Virus scanning recommended

## 🔄 Updates

### Application Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build app

# Check health
curl http://localhost:8000/health
```

### Database Migrations

```bash
# Run migrations
docker-compose exec app flask db upgrade

# Check migration status
docker-compose exec app flask db current
```

### Backup and Restore

#### Backup

```bash
# Database backup
docker-compose exec db pg_dump -U workshop_user workshop_certificates > backup.sql

# Uploads backup
tar -czf uploads_backup.tar.gz uploads/

# Certificates backup
tar -czf certificates_backup.tar.gz certificates/
```

#### Restore

```bash
# Database restore
docker-compose exec -T db psql -U workshop_user workshop_certificates < backup.sql

# Uploads restore
tar -xzf uploads_backup.tar.gz

# Certificates restore
tar -xzf certificates_backup.tar.gz
```

## 🚨 Troubleshooting

### Common Issues

#### Application Won't Start

```bash
# Check logs
docker-compose logs app

# Check health
curl http://localhost:8000/health

# Restart application
docker-compose restart app
```

#### Database Connection Issues

```bash
# Check database status
docker-compose exec db pg_isready -U workshop_user

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in ssl/cert.pem -text -noout

# Regenerate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/key.pem -out ssl/cert.pem \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"
```

### Performance Issues

#### High Memory Usage

```bash
# Check memory usage
docker stats

# Increase worker processes
# Edit docker-compose.yml and change --workers 4 to --workers 2
```

#### Slow Database Queries

```bash
# Check database performance
docker-compose exec db psql -U workshop_user workshop_certificates -c "SELECT * FROM pg_stat_activity;"
```

## 📈 Scaling

### Horizontal Scaling

For high traffic, consider:

1. **Load Balancer**: Use nginx or HAProxy
2. **Multiple App Instances**: Scale with `docker-compose up --scale app=3`
3. **Database Replication**: Master-slave PostgreSQL setup
4. **Redis Cluster**: For session storage and caching

### Vertical Scaling

Increase resources:

```yaml
# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
```

## 🔧 Maintenance

### Regular Tasks

- **Daily**: Check health endpoints and logs
- **Weekly**: Review error logs and performance metrics
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Full backup and disaster recovery test

### Updates

```bash
# Update dependencies
docker-compose exec app pip install --upgrade -r requirements.txt

# Update base images
docker-compose pull
docker-compose up -d
```

## 📞 Support

For issues:

1. Check the logs: `docker-compose logs -f`
2. Verify health: `curl http://localhost:8000/health`
3. Check configuration: Review `.env` and `docker-compose.yml`
4. Restart services: `docker-compose restart`

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed
- [ ] Database backups configured
- [ ] Monitoring and alerts set up
- [ ] Rate limiting configured
- [ ] Security headers enabled
- [ ] Health checks passing
- [ ] Logs being collected
- [ ] Backup strategy tested
- [ ] Disaster recovery plan ready 