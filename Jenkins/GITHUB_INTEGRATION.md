# 🔗 GitHub Integration Guide

## 📋 Setup Steps

### 1. Update Repository URL
Edit `workshop-setup.py` and update:
```python
self.github_repo = "your-username/ci-cd-chaos-workshop"  # Update this
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Add Jenkins workshop setup"
git push origin main
```

### 3. Test GitHub Integration
```bash
python3 workshop-setup.py test-github
```

## 🎯 Workshop Jobs

### Job 1: Docker Build Pipeline
- **Source**: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
- **Branch**: main
- **Jenkinsfile**: Jenkins/scenarios/01-docker-build/Jenkinsfile
- **Triggers**: Manual (for workshop)

### Job 2: Multi-Stage Pipeline (Future)
- **Source**: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
- **Branch**: main
- **Jenkinsfile**: Jenkins/scenarios/02-multi-stage/Jenkinsfile
- **Triggers**: Manual (for workshop)

## 🔧 Jenkins Configuration

### GitHub Credentials
1. Go to Jenkins → Manage Jenkins → Manage Credentials
2. Add GitHub credentials if needed
3. Configure GitHub webhook (optional)

### Webhook Setup (Optional)
1. Go to your GitHub repository
2. Settings → Webhooks
3. Add webhook: http://your-jenkins-url/github-webhook/
4. Select "Just the push event"

## 🎓 Workshop Flow

1. **Attendees clone repository**
2. **Run setup script** (one command)
3. **Access Jenkins** (http://localhost:8080)
4. **Run workshop jobs**
5. **See results and reports**

## 🚀 Benefits

- ✅ **Zero local dependencies** - Everything in Docker
- ✅ **Works anywhere** - Windows, macOS, Linux
- ✅ **GitHub integration** - Real source code management
- ✅ **Production ready** - Real CI/CD pipelines
- ✅ **Easy setup** - One command does everything
