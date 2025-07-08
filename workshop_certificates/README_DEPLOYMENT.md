# Quick Deploy to Render

This Flask app is configured for easy deployment to Render with WeasyPrint PDF generation.

## 🚀 Quick Start

### Option 1: Blueprint Deployment (Recommended)

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Deploy on Render**: 
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo
   - Click "Apply"

The `render.yaml` file handles everything automatically!

### Option 2: Manual Deployment

1. **Create Database**:
   - Render Dashboard → "New +" → "PostgreSQL"
   - Name: `workshop-db`
   - Plan: Starter (free)

2. **Deploy Web Service**:
   - Render Dashboard → "New +" → "Web Service"
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`

3. **Set Environment Variables**:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://... (from database)
   UPLOAD_FOLDER=uploads
   FLASK_ENV=production
   ```

## 📋 What's Included

- ✅ **Flask App** with SQLAlchemy database
- ✅ **WeasyPrint** PDF generation with all system dependencies
- ✅ **File uploads** with persistent storage
- ✅ **Admin panel** for user management
- ✅ **Static file serving** for MkDocs documentation
- ✅ **Production-ready** with gunicorn
- ✅ **Docker support** for containerized deployment

## 🧪 Testing

Run the deployment test:
```bash
cd workshop_certificates
python test_deployment.py
```

Or run the deployment script:
```bash
./deploy.sh
```

## 📚 Documentation

- **Full Guide**: See `DEPLOYMENT.md` for detailed instructions
- **Troubleshooting**: Check logs in Render dashboard
- **Support**: Render docs at https://render.com/docs

## 🔧 Configuration

The app automatically:
- Creates database tables on first run
- Sets up default configuration
- Handles file uploads in `uploads/` directory
- Serves static MkDocs files from `../site/`

## 🌐 URLs After Deployment

- **Main App**: `https://your-app.onrender.com/`
- **Documentation**: `https://your-app.onrender.com/docs/`
- **Admin Panel**: `https://your-app.onrender.com/admin/`
- **User Dashboard**: `https://your-app.onrender.com/app/`

## 💡 Tips

- **Free Tier**: 750 hours/month, sleeps after 15 min inactivity
- **Custom Domain**: Add in Render dashboard settings
- **SSL**: Automatically provided by Render
- **Scaling**: Upgrade to paid plan for always-on service

---

**Ready to deploy?** Just push to GitHub and use the Blueprint option! 🎉 