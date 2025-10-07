# 🚀 Pipeline Genesis - Your First Jenkins Pipeline

**Master Jenkins pipeline fundamentals in 5 minutes!**

Learn the core concepts of Jenkins pipelines through a simple, hands-on experience that builds your confidence step by step.

## 🎯 What You'll Learn

- **Pipeline Basics**: Understanding Jenkinsfile structure
- **Stages & Steps**: How to organize your pipeline
- **Build Triggers**: When and how pipelines run
- **Simple Automation**: Your first automated workflow

## 📁 Project Structure

```
01-pipeline-genesis/
├── README.md              # This guide
├── app.py                 # Simple Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Basic Docker setup
├── Jenkinsfile           # Your first Jenkins pipeline
└── tests/
    └── test_app.py       # Basic tests
```

## 🚀 Quick Start (5 Minutes Total)

### Step 1: The Application (1 minute)
A simple Flask app that greets users and shows system info.

```bash
# Run locally
python app.py
# Visit: http://localhost:5000
```

### Step 2: Your First Pipeline (2 minutes)
A clean, simple Jenkinsfile that anyone can understand:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Hello World') {
            steps {
                echo 'Hello, Jenkins Pipeline!'
            }
        }
        
        stage('Build App') {
            steps {
                echo 'Building the application...'
                sh 'python -m pip install -r requirements.txt'
            }
        }
        
        stage('Test App') {
            steps {
                echo 'Running tests...'
                sh 'python -m pytest tests/ -v'
            }
        }
        
        stage('Success!') {
            steps {
                echo '🎉 Your first pipeline completed successfully!'
            }
        }
    }
}
```

### Step 3: Run the Pipeline (1 minute)
1. Create Jenkins job
2. Point to this Jenkinsfile
3. Click "Build Now"
4. Watch the magic happen!

### Step 4: Understanding What Happened (1 minute)
- **Stage 1**: Simple greeting message
- **Stage 2**: Install dependencies
- **Stage 3**: Run basic tests
- **Stage 4**: Success celebration

## 🎮 Learning Experience

### What Makes This Special:
- ✅ **No Complexity**: Just the essentials
- ✅ **Visual Progress**: Clear stage-by-stage execution
- ✅ **Immediate Success**: Always works on first try
- ✅ **Real Application**: Not just "Hello World"

### Key Concepts You'll Master:
1. **Pipeline Structure**: agent, stages, steps
2. **Stage Organization**: Logical grouping of tasks
3. **Step Execution**: Individual commands and actions
4. **Build Flow**: How Jenkins executes your pipeline

## 🧪 The Application

A simple Flask app with:
- **Home page**: Welcome message
- **Health check**: `/health` endpoint
- **System info**: Shows Python version and environment

### API Endpoints:
- `GET /` - Welcome page
- `GET /health` - Health check
- `GET /info` - System information

## 🐳 Docker Integration

Simple Dockerfile for containerization:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## ⚙️ Jenkins Setup

### Quick Setup (Workshop Mode):
```bash
# 1. Start Jenkins
cd Jenkins
python3 setup-jenkins-complete.py setup

# 2. Access Jenkins
# Open http://localhost:8080

# 3. Create Pipeline Job
# - New Item → Pipeline
# - Name: "Pipeline Genesis"
# - Pipeline script from SCM
# - Repository: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
# - Script Path: Jenkins/jenkins-scenarios/01-pipeline-genesis/Jenkinsfile
```

### Manual Setup:
1. **Create New Pipeline Job**
2. **Configure Pipeline**:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - Script Path: `Jenkins/jenkins-scenarios/01-pipeline-genesis/Jenkinsfile`
3. **Save and Build**

## 🎯 Success Criteria

You've mastered this scenario when:
- ✅ You understand what a Jenkinsfile is
- ✅ You can identify stages and steps
- ✅ Your pipeline runs successfully
- ✅ You can explain what each stage does
- ✅ You feel confident about Jenkins basics

## 🚀 Next Steps

After completing this scenario:
1. **Try modifying the pipeline** - Add your own stages
2. **Experiment with different steps** - Try new commands
3. **Move to Scenario 2** - Test Master with TestContainers
4. **Build your confidence** - You're now a Jenkins beginner!

## 💡 Pro Tips

- **Start Simple**: Don't overcomplicate your first pipeline
- **Read the Logs**: Jenkins logs show exactly what's happening
- **One Stage at a Time**: Focus on one stage before moving to the next
- **Ask Questions**: Understanding is more important than speed

---

**Ready to build your first Jenkins pipeline? Let's go! 🚀**
