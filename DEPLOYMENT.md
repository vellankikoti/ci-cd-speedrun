# 🚀 Deployment Guide for CI/CD Chaos Workshop

This guide will help you deploy your MkDocs documentation site to Render.

## 📋 Prerequisites

- A Render account (free tier available)
- Your repository connected to GitHub/GitLab
- Python 3.9+ support

## 🎯 Deployment Options

### Option 1: Static Site (Recommended)

This is the most efficient option for documentation sites.

1. **Connect your repository to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Static Site"
   - Connect your GitHub/GitLab repository

2. **Configure the deployment**
   - **Name**: `ci-cd-chaos-workshop`
   - **Build Command**: 
     ```bash
     python -m pip install --upgrade pip && pip install mkdocs mkdocs-material && mkdocs build
     ```
   - **Publish Directory**: `site`
   - **Environment**: Static Site

3. **Deploy**
   - Click "Create Static Site"
   - Render will automatically build and deploy your site

### Option 2: Web Service

If you need server-side functionality:

1. **Connect your repository to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository

2. **Configure the deployment**
   - **Name**: `ci-cd-chaos-workshop`
   - **Environment**: Python
   - **Build Command**: 
     ```bash
     python -m pip install --upgrade pip && pip install -r requirements.txt && mkdocs build
     ```
   - **Start Command**: 
     ```bash
     mkdocs serve --dev-addr=0.0.0.0:$PORT --no-livereload
     ```

3. **Environment Variables**
   - `PYTHON_VERSION`: `3.9`

## 🔧 Configuration Files

### render.yaml
```yaml
services:
  - type: web
    name: ci-cd-chaos-workshop
    env: static
    buildCommand: |
      python -m pip install --upgrade pip
      pip install mkdocs mkdocs-material
      mkdocs build
    staticPublishPath: ./site
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
    plan: free
    autoDeploy: true
```

### requirements.txt
```
mkdocs==1.6.1
mkdocs-material==9.6.14
mkdocs-minify-plugin==0.7.2
```

## 🌐 Custom Domain (Optional)

1. **Add Custom Domain**
   - Go to your Render dashboard
   - Select your service
   - Go to "Settings" → "Custom Domains"
   - Add your domain

2. **Configure DNS**
   - Add a CNAME record pointing to your Render URL
   - Or use Render's automatic DNS configuration

## 🔄 Auto-Deployment

- **GitHub Integration**: Automatic deployments on push to main branch
- **Preview Deployments**: Automatic preview deployments for pull requests
- **Manual Deployments**: Available through Render dashboard

## 📊 Monitoring

- **Build Logs**: Available in Render dashboard
- **Performance**: Static sites are served via CDN
- **Analytics**: Available through Render dashboard

## 🛠️ Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Python version compatibility
   - Verify all dependencies are in requirements.txt
   - Check mkdocs.yml syntax

2. **Site Not Loading**
   - Verify staticPublishPath is correct (`./site`)
   - Check build logs for errors
   - Ensure mkdocs build completes successfully

3. **Missing Assets**
   - Verify all assets are in the docs directory
   - Check mkdocs.yml navigation configuration
   - Ensure all referenced files exist

### Local Testing

Test your deployment locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Build the site
mkdocs build

# Test locally
mkdocs serve
```

## 🎉 Success!

Once deployed, your documentation will be available at:
`https://your-app-name.onrender.com`

---

**Happy Deploying! 🚀** 