# 🧪 Test Master - Advanced Testing with TestContainers

**Master TestContainers integration in Jenkins pipelines!**

Learn how to run real database tests in your Jenkins pipeline using TestContainers - no more mocking, just real integration testing!

## 🎯 What You'll Learn

- **TestContainers Basics**: Real database testing in containers
- **Integration Testing**: Test with actual databases, not mocks
- **Parallel Testing**: Run tests against multiple databases simultaneously
- **Test Reporting**: Generate beautiful test reports and coverage

## 📁 Project Structure

```
02-test-master/
├── README.md              # This guide
├── app.py                 # Flask app with database integration
├── requirements.txt       # Python dependencies including testcontainers
├── Dockerfile            # Multi-stage Docker build
├── Jenkinsfile           # TestContainers-enabled pipeline
├── database.py           # Database connection and models
└── tests/
    ├── test_app.py       # Basic application tests
    ├── test_database.py  # Database integration tests
    └── test_containers.py # TestContainers integration tests
```

## 🚀 Quick Start (5 Minutes Total)

### Step 1: The Application (1 minute)
A Flask app that connects to a real database and performs CRUD operations.

```bash
# Run locally (requires Docker)
python app.py
# Visit: http://localhost:5000
```

### Step 2: TestContainers Magic (2 minutes)
Real database testing without setup complexity:

```python
from testcontainers.postgres import PostgresContainer
from testcontainers.mysql import MySqlContainer

def test_with_postgres():
    with PostgresContainer("postgres:13") as postgres:
        # Real PostgreSQL database for testing!
        connection_string = postgres.get_connection_url()
        # Your tests here...
```

### Step 3: Jenkins Pipeline (1 minute)
Pipeline that runs tests against multiple databases:

```groovy
stage('🧪 Test with TestContainers') {
    steps {
        sh 'python -m pytest tests/test_containers.py -v --tb=short'
    }
}
```

### Step 4: Understanding the Power (1 minute)
- **Real Databases**: No more mocking - test with actual PostgreSQL, MySQL, Redis
- **Parallel Execution**: Test against multiple databases simultaneously
- **Isolated Tests**: Each test gets a fresh database instance
- **Jenkins Integration**: Works seamlessly in CI/CD pipelines

## 🎮 Learning Experience

### What Makes This Special:
- ✅ **Real Integration**: Test with actual databases, not mocks
- ✅ **Multiple Databases**: PostgreSQL, MySQL, Redis in one pipeline
- ✅ **Parallel Testing**: Fast execution with multiple database types
- ✅ **Zero Setup**: TestContainers handles all database setup

### Key Concepts You'll Master:
1. **TestContainers**: Container-based testing framework
2. **Database Testing**: Real integration testing patterns
3. **Parallel Execution**: Running tests simultaneously
4. **Test Isolation**: Each test gets fresh database state

## 🧪 The Application

A Flask app with database integration:
- **User Management**: Create, read, update, delete users
- **Database Support**: PostgreSQL, MySQL, Redis
- **Health Checks**: Database connectivity monitoring
- **API Endpoints**: RESTful API for user operations

### API Endpoints:
- `GET /` - Application dashboard
- `GET /health` - Health check with database status
- `GET /users` - List all users
- `POST /users` - Create new user
- `GET /users/<id>` - Get specific user
- `PUT /users/<id>` - Update user
- `DELETE /users/<id>` - Delete user

## 🐳 Docker Integration

Multi-stage Dockerfile for optimized builds:
```dockerfile
# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## ⚙️ Jenkins Pipeline

### TestContainers-Enabled Pipeline:
```groovy
pipeline {
    agent any
    
    stages {
        stage('🧪 Test with TestContainers') {
            parallel {
                stage('PostgreSQL Tests') {
                    steps {
                        sh 'python -m pytest tests/test_containers.py::test_postgres -v'
                    }
                }
                stage('MySQL Tests') {
                    steps {
                        sh 'python -m pytest tests/test_containers.py::test_mysql -v'
                    }
                }
                stage('Redis Tests') {
                    steps {
                        sh 'python -m pytest tests/test_containers.py::test_redis -v'
                    }
                }
            }
        }
    }
}
```

## 🚀 Jenkins Setup

### Quick Setup (Workshop Mode):
```bash
# 1. Start Jenkins
cd Jenkins
python3 setup-jenkins-complete.py setup

# 2. Access Jenkins
# Open http://localhost:8080

# 3. Create Pipeline Job
# - New Item → Pipeline
# - Name: "Test Master"
# - Pipeline script from SCM
# - Repository: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
# - Script Path: Jenkins/jenkins-scenarios/02-test-master/Jenkinsfile
```

### Manual Setup:
1. **Create New Pipeline Job**
2. **Configure Pipeline**:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - Script Path: `Jenkins/jenkins-scenarios/02-test-master/Jenkinsfile`
3. **Save and Build**

## 🎯 Success Criteria

You've mastered this scenario when:
- ✅ You understand what TestContainers are
- ✅ You can run tests against real databases
- ✅ Your pipeline tests multiple databases in parallel
- ✅ You can explain the benefits of integration testing
- ✅ You feel confident about database testing

## 🚀 Next Steps

After completing this scenario:
1. **Try different databases** - Add MongoDB, Elasticsearch
2. **Experiment with parallel testing** - Optimize test execution
3. **Move to Scenario 3** - Docker Ninja with advanced containerization
4. **Build your confidence** - You're now a testing expert!

## 💡 Pro Tips

- **Start Simple**: Begin with one database, then add more
- **Use Parallel Execution**: Speed up your test suite
- **Monitor Resources**: TestContainers can be resource-intensive
- **Clean Up**: Always clean up containers after tests

---

**Ready to master TestContainers? Let's test like a pro! 🧪**
