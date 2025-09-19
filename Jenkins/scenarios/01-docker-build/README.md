# 🐳 Docker Build Pipeline - Scenario 1

A complete, production-ready Docker build pipeline demonstrating best practices for containerized applications.

## 🎯 Overview

This scenario demonstrates a comprehensive Docker build pipeline with:
- **Real Flask Application** - A working web application with API endpoints
- **Automated Testing** - Comprehensive test suite with coverage reporting
- **Docker Containerization** - Multi-stage Dockerfile with security best practices
- **Jenkins Pipeline** - Complete CI/CD pipeline with validation, testing, and deployment
- **Local Execution** - Works seamlessly when run locally

## 📁 Project Structure

```
01-docker-build/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Multi-stage Docker build
├── Jenkinsfile           # Jenkins CI/CD pipeline
├── README.md             # This documentation
└── tests/
    └── test_app.py       # Comprehensive test suite
```

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Access the application:**
   - Main page: http://localhost:5000
   - Health check: http://localhost:5000/health
   - API info: http://localhost:5000/api/info

4. **Run tests:**
   ```bash
   python -m pytest tests/ -v
   ```

### Docker Build

1. **Build the image:**
   ```bash
   docker build -t docker-build-demo .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 docker-build-demo
   ```

3. **Test the container:**
   ```bash
   curl http://localhost:5000/health
   ```

## 🧪 Testing

### Test Coverage

The application includes comprehensive tests covering:
- **Health endpoints** - Basic health checks
- **API endpoints** - All REST API functionality
- **Error handling** - Edge cases and error scenarios
- **Performance** - Response time validation
- **Integration** - End-to-end workflow testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test
python -m pytest tests/test_app.py::TestHealthEndpoints -v
```

### Test Reports

Tests generate multiple report formats:
- **HTML Report** - `test-reports/report.html`
- **Coverage Report** - `coverage-reports/index.html`
- **JUnit XML** - `test-reports/junit.xml`

## 🐳 Docker Features

### Multi-stage Build

The Dockerfile uses a multi-stage build process:
1. **Builder stage** - Installs dependencies and builds the application
2. **Production stage** - Creates a minimal runtime image

### Security Features

- **Non-root user** - Application runs as non-root user
- **Minimal base image** - Uses Python slim image
- **Health checks** - Built-in container health monitoring
- **Security scanning** - Vulnerability scanning in pipeline

### Build Arguments

The Docker build supports several build arguments:
- `APP_VERSION` - Application version
- `BUILD_TIME` - Build timestamp
- `ENVIRONMENT` - Target environment

## 🔄 Jenkins Pipeline

### Pipeline Stages

1. **Checkout** - Fetch source code
2. **Validate** - Verify application structure
3. **Install Dependencies** - Install Python packages
4. **Test** - Run automated tests with reporting
5. **Build Docker Image** - Create containerized application
6. **Test Docker Image** - Validate container functionality
7. **Security Scan** - Check for vulnerabilities
8. **Deploy** - Deploy to target environment
9. **Push to Registry** - Push image to container registry

### Pipeline Parameters

- **ENVIRONMENT** - Target environment (development/staging/production)
- **RUN_TESTS** - Enable/disable test execution
- **PUSH_TO_REGISTRY** - Enable/disable registry push

### Local Jenkins Execution

To run the pipeline locally:

1. **Start Jenkins:**
   ```bash
   docker run -d --name jenkins-workshop \
     -p 8080:8080 -p 50000:50000 \
     -v jenkins_home:/var/jenkins_home \
     -v /var/run/docker.sock:/var/run/docker.sock \
     jenkins/jenkins:lts
   ```

2. **Create a new job:**
   - Go to http://localhost:8080
   - Create "New Item" → "Pipeline"
   - Point to this directory's Jenkinsfile

3. **Run the pipeline:**
   - Click "Build Now"
   - Monitor the build progress

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
# Click "🎓 Workshop - Docker Build Pipeline" → "Build Now"
```

### Manual Jenkins Job Creation (Production Mode)

#### Step 1: Create New Pipeline Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `Docker Build Pipeline - Production`
4. **Select "Pipeline"** and click "OK"

#### Step 2: Configure Pipeline
1. **Description**: "Complete Docker build pipeline with testing and deployment"
2. **Pipeline section**:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - **Branches to build**: `*/main` (or your preferred branch)
   - **Script Path**: `Jenkins/scenarios/01-docker-build/Jenkinsfile`

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

## 🌐 API Endpoints

### Health Endpoints

- `GET /health` - Basic health check
- `GET /api/status` - Detailed status information

### API Endpoints

- `GET /api/info` - Application information
- `POST /api/echo` - Echo test endpoint
- `GET /api/load-test` - Performance test endpoint

### Web Interface

- `GET /` - Main application page with status dashboard

## 🔧 Configuration

### Environment Variables

- `APP_VERSION` - Application version (default: 1.0.0)
- `BUILD_TIME` - Build timestamp
- `ENVIRONMENT` - Target environment (default: development)
- `PORT` - Application port (default: 5000)

### Docker Configuration

The application supports various Docker configurations:
- **Port mapping** - Configurable port exposure
- **Environment variables** - Runtime configuration
- **Health checks** - Container health monitoring
- **Resource limits** - CPU and memory constraints

## 📊 Monitoring

### Health Checks

The application provides multiple health check endpoints:
- **Basic health** - `/health`
- **Detailed status** - `/api/status`
- **Container health** - Docker health check

### Metrics

The application exposes various metrics:
- **Uptime** - Application runtime
- **Response times** - API endpoint performance
- **Build information** - Version and build details

## 🚀 Deployment

### Local Deployment

```bash
# Build and run locally
docker build -t docker-build-demo .
docker run -p 5000:5000 docker-build-demo
```

### Production Deployment

The pipeline generates deployment configurations:
- **Docker Compose** - `deployments/{environment}/docker-compose.yml`
- **Environment-specific** - Different configs per environment
- **Health monitoring** - Built-in health checks

## 🛠️ Development

### Code Quality

The project includes code quality tools:
- **Black** - Code formatting
- **Flake8** - Linting
- **Pytest** - Testing framework
- **Coverage** - Test coverage reporting

### Adding Features

To add new features:
1. Update `app.py` with new functionality
2. Add tests in `tests/test_app.py`
3. Update `requirements.txt` if needed
4. Test locally and in Docker
5. Update documentation

## 🐛 Troubleshooting

### Common Issues

1. **Port conflicts** - Change the port in environment variables
2. **Docker build failures** - Check Docker daemon is running
3. **Test failures** - Verify all dependencies are installed
4. **Jenkins pipeline failures** - Check Jenkins logs and Docker access

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export ENVIRONMENT=development
python app.py
```

## 📈 Performance

### Optimization Features

- **Multi-stage builds** - Reduced image size
- **Layer caching** - Faster builds
- **Health checks** - Container monitoring
- **Resource limits** - Controlled resource usage

### Benchmarks

The application includes performance tests:
- **Response time** - API endpoint performance
- **Load testing** - Basic load test endpoint
- **Memory usage** - Container resource monitoring

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
1. **Explore other scenarios** - Move to scenario 2 (TestContainers)
2. **Customize the application** - Add your own features
3. **Extend the pipeline** - Add more stages or integrations
4. **Deploy to cloud** - Use cloud container services
5. **Monitor in production** - Add monitoring and alerting

---

**This scenario demonstrates a complete, production-ready Docker build pipeline that works seamlessly both locally and in Jenkins! 🚀**