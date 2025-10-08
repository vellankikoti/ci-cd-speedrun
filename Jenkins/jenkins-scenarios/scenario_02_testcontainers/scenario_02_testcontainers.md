# TestContainers Integration

Integration testing with TestContainers

## Overview

This scenario demonstrates integration testing with testcontainers in a Jenkins pipeline.

## Files

- `Jenkinsfile` - Jenkins pipeline definition
- `Dockerfile` - Docker container definition
- `requirements.txt` - Python dependencies
- `tests/` - Test files directory

## Usage

### Quick Setup (Workshop Mode)
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
# Click "🎓 Workshop - TestContainers Integration" → "Build Now"
```

### Manual Jenkins Job Creation (Production Mode)

#### Step 1: Create New Pipeline Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `TestContainers Integration - Production`
4. **Select "Pipeline"** and click "OK"

#### Step 2: Configure Pipeline
1. **Description**: "Complete testcontainers integration pipeline with testing and deployment"
2. **Pipeline section**:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - **Branches to build**: `*/main` (or your preferred branch)
   - **Script Path**: `Jenkins/scenarios/02-testcontainers/Jenkinsfile`

#### Step 3: Configure Build Triggers (Optional)
- **GitHub hook trigger for GITScm polling** (if using webhooks)
- **Poll SCM** with schedule: `H/5 * * * *` (every 5 minutes)

#### Step 4: Configure Build Environment (Optional)
- **Delete workspace before build starts**
- **Add timestamps to the Console Output**

#### Step 5: Save and Run
1. **Click "Save"**
2. **Click "Build Now"**
3. **Monitor the pipeline execution**

### Pipeline Stages Overview

The Jenkinsfile includes these production-ready stages:

1. **Checkout Code** - Fetches source code from GitHub
2. **Build Docker Image** - Creates production-ready Docker image
3. **Run Unit and Integration Tests** - Executes comprehensive test suite with TestContainers
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



## 🏭 Production Jenkins Job Setup

### Quick Setup (Workshop Mode)
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
# Click "🎓 Workshop - 02 Testcontainers" → "Build Now"
```

### Manual Jenkins Job Creation (Production Mode)

#### Step 1: Create New Pipeline Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `02 Testcontainers - Production`
4. **Select "Pipeline"** and click "OK"

#### Step 2: Configure Pipeline
1. **Description**: "Complete 02 testcontainers pipeline with testing and deployment"
2. **Pipeline section**:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - **Branches to build**: `*/main` (or your preferred branch)
   - **Script Path**: `Jenkins/scenarios/02-testcontainers/Jenkinsfile`

#### Step 3: Configure Build Triggers (Optional)
- **GitHub hook trigger for GITScm polling** (if using webhooks)
- **Poll SCM** with schedule: `H/5 * * * *` (every 5 minutes)

#### Step 4: Configure Build Environment (Optional)
- **Delete workspace before build starts**
- **Add timestamps to the Console Output**

#### Step 5: Save and Run
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


## Testing

Run tests locally:
```bash
python -m pytest tests/ -v
```

## Docker

Build and run locally:
```bash
docker build --no-cache -t 02-testcontainers .
docker run 02-testcontainers
```
