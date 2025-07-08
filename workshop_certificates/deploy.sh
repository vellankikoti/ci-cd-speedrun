#!/bin/bash

# Workshop Certificates Deployment Script
# This script helps prepare and deploy the Flask app to Render

set -e

echo "🚀 Workshop Certificates Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the workshop_certificates directory."
    exit 1
fi

# Check if required files exist
echo "📋 Checking required files..."
required_files=("requirements.txt" "Dockerfile" "render.yaml" ".dockerignore")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file found"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Check Python dependencies
echo "🐍 Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
else
    echo "❌ Python 3 not found"
    exit 1
fi

# Test WeasyPrint installation
echo "📄 Testing WeasyPrint..."
python3 -c "from weasyprint import HTML; print('✅ WeasyPrint OK')" 2>/dev/null || {
    echo "❌ WeasyPrint not available. Install system dependencies first:"
    echo "   sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev"
    exit 1
}

# Check if git is available
if command -v git &> /dev/null; then
    echo "✅ Git found"
    echo "📝 Current git status:"
    git status --porcelain || echo "   No changes to commit"
else
    echo "⚠️  Git not found - make sure to commit your changes manually"
fi

# Create uploads directory if it doesn't exist
if [ ! -d "uploads" ]; then
    echo "📁 Creating uploads directory..."
    mkdir -p uploads
    echo "✅ uploads directory created"
fi

# Test local Flask app
echo "🧪 Testing Flask app..."
export FLASK_ENV=development
export SECRET_KEY=test-secret-key
export DATABASE_URL=sqlite:///test.db
export UPLOAD_FOLDER=uploads

python3 -c "
from app import create_app
app = create_app()
print('✅ Flask app created successfully')
" 2>/dev/null || {
    echo "❌ Flask app test failed"
    exit 1
}

echo ""
echo "🎉 All checks passed! Your app is ready for deployment."
echo ""
echo "📋 Next steps:"
echo "1. Commit your changes to Git:"
echo "   git add ."
echo "   git commit -m 'Prepare for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Deploy to Render:"
echo "   - Go to https://dashboard.render.com/"
echo "   - Click 'New +' → 'Blueprint'"
echo "   - Connect your GitHub repository"
echo "   - Click 'Apply' to deploy"
echo ""
echo "3. Or deploy manually:"
echo "   - Create PostgreSQL database on Render"
echo "   - Create Web Service pointing to this directory"
echo "   - Set environment variables (see DEPLOYMENT.md)"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT.md" 