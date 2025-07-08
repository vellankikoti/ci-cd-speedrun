# Deploying Workshop Certificates to Render

This guide will help you deploy your Flask application with WeasyPrint PDF generation to Render.

## Prerequisites

1. A GitHub account
2. A Render account (free tier available)
3. Your code pushed to a GitHub repository

## Option 1: Deploy with render.yaml (Recommended)

### Step 1: Prepare Your Repository

1. Ensure your repository structure looks like this:
   ```
   workshop_certificates/
   ├── app.py
   ├── requirements.txt
   ├── Dockerfile
   ├── render.yaml
   ├── .dockerignore
   ├── auth.py
   ├── views.py
   ├── models.py
   ├── certificate_generator.py
   ├── markdown_parser.py
   ├── init_db.py
   └── templates/
   ```

2. Make sure all files are committed and pushed to GitHub.

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to deploy

The `render.yaml` file will:
- Create a PostgreSQL database
- Deploy your Flask app
- Set up environment variables
- Configure the build and start commands

## Option 2: Manual Deployment

### Step 1: Create Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" and select "PostgreSQL"
3. Choose "Starter" plan (free)
4. Name it `workshop-db`
5. Note the connection string

### Step 2: Deploy Web Service

1. Click "New +" and select "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `workshop-certificates`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`
   - **Plan**: Starter (free)

### Step 3: Set Environment Variables

Add these environment variables in the Render dashboard:

| Key | Value | Description |
|-----|-------|-------------|
| `SECRET_KEY` | `your-secret-key-here` | Flask secret key |
| `DATABASE_URL` | `postgresql://...` | From your database |
| `UPLOAD_FOLDER` | `uploads` | Upload directory |
| `FLASK_ENV` | `production` | Production environment |

## Environment Variables

### Required Variables

- `SECRET_KEY`: A secure random string for Flask sessions
- `DATABASE_URL`: PostgreSQL connection string (auto-provided by Render)
- `UPLOAD_FOLDER`: Directory for file uploads (default: `uploads`)
- `FLASK_ENV`: Set to `production`

### Optional Variables

- `LOG_LEVEL`: Set to `INFO` or `DEBUG`
- `ADMIN_EMAIL`: Admin user email for initial setup

## Database Setup

The application will automatically:
1. Create database tables on first run
2. Set up default configuration
3. Create admin user if needed

## File Uploads

- Uploads are stored in the `uploads/` directory
- Render provides persistent disk storage
- Files are served statically by Flask

## PDF Generation

WeasyPrint is configured with all necessary system dependencies:
- Cairo graphics library
- Pango text layout
- GDK-PixBuf image loading
- Font rendering support

## Monitoring and Logs

1. **View Logs**: Go to your service dashboard and click "Logs"
2. **Monitor Performance**: Check the "Metrics" tab
3. **Debug Issues**: Use the "Shell" feature for debugging

## Troubleshooting

### Common Issues

1. **Build Fails**: Check that all dependencies are in `requirements.txt`
2. **WeasyPrint Errors**: Ensure system dependencies are installed (handled by Dockerfile)
3. **Database Connection**: Verify `DATABASE_URL` is correct
4. **File Uploads**: Check `UPLOAD_FOLDER` permissions

### Debug Commands

```bash
# Check if WeasyPrint works
python -c "from weasyprint import HTML; print('WeasyPrint OK')"

# Test database connection
python -c "from app import create_app; app = create_app(); print('DB OK')"

# Check environment
python -c "import os; print(os.environ.get('DATABASE_URL'))"
```

## Scaling

- **Free Tier**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Plans**: Always-on, custom domains, SSL certificates
- **Auto-scaling**: Available on paid plans

## Custom Domain

1. Go to your service dashboard
2. Click "Settings" → "Custom Domains"
3. Add your domain
4. Configure DNS records as instructed

## SSL Certificate

Render automatically provides SSL certificates for all services.

## Backup Strategy

1. **Database**: Render provides automatic PostgreSQL backups
2. **Files**: Uploads are stored on persistent disk
3. **Code**: Version control with GitHub

## Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **File Uploads**: Validate file types and sizes
3. **Database**: Use connection pooling for production
4. **HTTPS**: Always enabled on Render

## Performance Optimization

1. **Database**: Use connection pooling
2. **Static Files**: Serve via CDN for large files
3. **Caching**: Implement Redis for session storage
4. **Workers**: Adjust gunicorn workers based on load

## Support

- **Render Documentation**: https://render.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **WeasyPrint Documentation**: https://weasyprint.readthedocs.io/

## Next Steps

After deployment:
1. Test all features (upload, PDF generation, admin panel)
2. Set up monitoring and alerts
3. Configure custom domain if needed
4. Set up automated backups
5. Monitor performance and scale as needed 