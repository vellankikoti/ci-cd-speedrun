# 🚀 Deployment Guide for CI/CD Chaos Workshop

This guide will help you deploy your MkDocs documentation site to Render.

## 📋 Prerequisites

- A Render account (free tier available)
- Your repository connected to GitHub/GitLab

## 🎯 Deployment Method

### Static Site Deployment (Recommended)

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

## 🔧 Manual Deployment (Alternative)

If you prefer to build locally and upload:

```bash
# Install mkdocs
pip install mkdocs mkdocs-material

# Build the site
mkdocs build

# The site will be in the ./site directory
# Upload the contents of ./site to any static hosting service
```

## 📁 Files Structure

```
ci-cd-chaos-workshop/
├── docs/                    # Your documentation
├── mkdocs.yml              # MkDocs configuration
├── render.yaml             # Render configuration
└── site/                   # Built static site (generated)
```

## 🎉 Benefits of This Approach

- ✅ **No Docker complexity** - Simple Python installation
- ✅ **Fast builds** - Minimal dependencies
- ✅ **Easy maintenance** - Standard MkDocs workflow
- ✅ **Cost effective** - Free tier friendly
- ✅ **Automatic deployments** - Git-based triggers

## 🚀 Your Site Will Be Available At

Once deployed, your site will be available at:
`https://your-site-name.onrender.com`

## 🔄 Continuous Deployment

Every time you push to your main branch, Render will automatically rebuild and deploy your site! 