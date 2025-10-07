# 🚀 Scenario Template - [Scenario Name]

## 🎯 Goal

[Brief description of what this scenario demonstrates and teaches]

## 📦 Application Overview

[Description of the application, its features, and purpose]

## 🧪 Testing

[Description of the testing approach and test coverage]

## 🐳 Docker Setup

[Description of Docker configuration and multi-stage builds]

## ⚙️ Jenkins Pipeline

[Description of the Jenkins pipeline stages and features]

## 🚀 How to Use

### 1. Local Development & Testing

```bash
# Navigate to the scenario directory
cd Jenkins/scenarios/[scenario-name]

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application locally
python app.py

# Run tests locally
pytest tests/ -v --cov=app --cov-report=term-missing --html=report.html --self-contained-html
```

### 2. Docker Build & Run

```bash
# Navigate to the scenario directory
cd Jenkins/scenarios/[scenario-name]

# Build the Docker image
docker build -t [scenario-name]-demo:latest .

# Run the Docker container
docker run -d --name test-container -p 5000:5000 [scenario-name]-demo:latest

# Test the application
curl http://localhost:5000/health

# Clean up
docker rm -f test-container
```

### 3. Jenkins Pipeline Execution

#### Quick Setup (Workshop Mode)
```bash
# 1. Clone the repository
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop

# 2. Start Jenkins (one command!)
cd Jenkins
python3 setup-jenkins-complete.py setup

# 3. Access Jenkins
# Open http://localhost:8080
# Complete the setup wizard

# 4. Run the pre-configured workshop job
# Click "🎓 Workshop - [Scenario Name]" → "Build Now"
```

#### Manual Jenkins Job Creation (Production Mode)

##### Step 1: Create New Pipeline Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `[Scenario Name] - Production`
4. **Select "Pipeline"** and click "OK"

##### Step 2: Configure Pipeline
1. **Description**: "[Brief description of the pipeline]"
2. **Pipeline section**:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - **Branches to build**: `*/main` (or your preferred branch)
   - **Script Path**: `Jenkins/scenarios/[scenario-name]/Jenkinsfile`

##### Step 3: Configure Build Triggers (Optional)
- **GitHub hook trigger for GITScm polling** (if using webhooks)
- **Poll SCM** with schedule: `H/5 * * * *` (every 5 minutes)

##### Step 4: Configure Build Environment (Optional)
- **Delete workspace before build starts**
- **Add timestamps to the Console Output**

##### Step 5: Save and Run
1. **Click "Save"**
2. **Click "Build Now"**
3. **Monitor the pipeline execution**

### Pipeline Stages Overview

The Jenkinsfile includes these production-ready stages:

1. **Checkout Code** - Fetches source code from GitHub
2. **Build Docker Image** - Creates production-ready Docker image
3. **Run Unit and Integration Tests** - Executes comprehensive test suite
4. **Security Scan** - Scans Docker image for vulnerabilities
5. **Push Docker Image** - Pushes to Docker registry (configurable)
6. **Deploy to Staging** - Deploys to staging environment
7. **Run Acceptance Tests** - Validates staging deployment
8. **Approve for Production** - Manual approval gate
9. **Deploy to Production** - Production deployment

### Monitoring and Debugging

#### View Pipeline Progress
- Go to the job page
- Click on the build number
- View "Pipeline Steps" for detailed execution

#### Check Logs
- Click on any stage to see detailed logs
- Use "Console Output" for full build log

#### View Reports
- **Test Results**: JUnit test reports
- **Coverage Report**: Code coverage metrics
- **HTML Reports**: Detailed test and build reports

#### Troubleshooting
```bash
# Check Jenkins container logs
docker logs jenkins-workshop

# Check Docker daemon
docker info

# Verify Git access
docker exec jenkins-workshop git --version

# Check Jenkins workspace
docker exec jenkins-workshop ls -la /var/jenkins_home/workspace/
```

### Advanced Configuration

#### Environment Variables
Configure these in Jenkins → Manage Jenkins → Configure System → Global Properties:

- `DOCKER_REGISTRY`: Your Docker registry URL
- `DOCKER_CREDENTIAL_ID`: Jenkins credential ID for Docker registry
- `STAGING_URL`: Staging environment URL
- `PRODUCTION_URL`: Production environment URL

#### Credentials Setup
1. **Jenkins → Manage Jenkins → Manage Credentials**
2. **Add credentials for**:
   - Docker registry login
   - GitHub access (if using private repos)
   - Cloud provider access (AWS, Azure, GCP)

#### Webhook Configuration (Optional)
1. **GitHub Repository → Settings → Webhooks**
2. **Add webhook**: `http://your-jenkins-url/github-webhook/`
3. **Select events**: "Just the push event"
4. **Test webhook** to ensure connectivity

## 🌐 API Endpoints

[Document the API endpoints and their functionality]

## 🧪 Testing Details

[Detailed testing information including test cases and coverage]

## 🐳 Docker Configuration

[Detailed Docker configuration and optimization]

## ⚙️ Jenkins Pipeline Details

[Detailed Jenkins pipeline configuration and stages]

## 🔧 Configuration

[Configuration options and environment variables]

## 🚀 Deployment

[Deployment instructions and options]

## 📊 Monitoring

[Monitoring and observability setup]

## 🔍 Troubleshooting

[Common issues and solutions]

## 📈 Performance

[Performance considerations and optimization]

## 🎉 Success Criteria

This scenario is successful when:
- ✅ Application runs locally without errors
- ✅ All tests pass with good coverage
- ✅ Docker image builds successfully
- ✅ Container runs and responds to health checks
- ✅ Jenkins pipeline executes all stages
- ✅ API endpoints return expected responses
- ✅ Web interface displays correctly

## 📚 Next Steps

After completing this scenario:
1. **Explore other scenarios** - Move to the next scenario
2. **Customize the application** - Add your own features
3. **Extend the pipeline** - Add more stages or integrations
4. **Deploy to cloud** - Use cloud container services

---

**This scenario demonstrates [what it demonstrates]! 🚀**
