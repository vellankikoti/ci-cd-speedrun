# TestContainers Integration

Real TestContainers integration with PostgreSQL in Jenkins

## Overview

This scenario demonstrates real TestContainers integration with PostgreSQL databases in a Jenkins job. Unlike traditional mocking, this uses actual database containers for authentic integration testing.

## Files

- `setup-jenkins-job.py` - Jenkins job setup script
- `demo.py` - Educational workshop script
- `demo_testcontainers.py` - Interactive TestContainers demo
- `database.py` - PostgreSQL database manager with TestContainers
- `app.py` - Flask application with PostgreSQL integration
- `Dockerfile` - Docker container definition
- `docker-compose.test.yml` - TestContainers setup
- `requirements.txt` - TestContainers and PostgreSQL dependencies
- `tests/` - Comprehensive test suites

## Quick Start

### Workshop Mode
```bash
# 1. Start Jenkins
cd Jenkins
python3 jenkins-setup.py setup

# 2. Run educational workshop
cd jenkins-scenarios/scenario_02_testcontainers
python3 demo.py

# 3. Or create Jenkins job automatically
python3 setup-jenkins-job.py
```

### Manual Jenkins Job Creation

#### Step 1: Create Freestyle Job
1. **Access Jenkins** at `http://localhost:8080`
2. **Click "New Item"**
3. **Enter job name**: `TestContainers Integration`
4. **Select "Freestyle project"** and click "OK"

#### Step 2: Configure Job
1. **Description**: "TestContainers Integration Demo - Real database testing with PostgreSQL containers"
2. **Check "This project is parameterized"**:
   - Add String Parameter: `DB_TYPE` (default: testcontainers)
   - Add String Parameter: `TEST_MODE` (default: all)
3. **Source Code Management**:
   - Select "Git"
   - Repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
   - Branch: `*/docker-test`
4. **Build Steps**:
   - Add "Execute shell" step
   - Copy the build script from `setup-jenkins-job.py`

#### Step 3: Save and Run
1. **Click "Save"**
2. **Click "Build with Parameters"**
3. **Choose test mode and click "Build"**

## TestContainers Job Modes

The Jenkins job includes these comprehensive testing modes:

1. **Demo Mode** - Interactive TestContainers demonstration
2. **Tests Mode** - Run TestContainers integration tests
3. **App Tests Mode** - Run application tests with PostgreSQL
4. **Docker Mode** - Run with Docker Compose integration
5. **All Mode** - Complete test suite execution

## What TestContainers Does

- **Real PostgreSQL Containers**: Creates actual database containers, not mocks
- **Automatic Cleanup**: Containers are automatically destroyed after tests
- **Isolated Testing**: Each test run gets a fresh database instance
- **Production-like Testing**: Tests run against real database behavior
- **Concurrent Testing**: Multiple tests can run in parallel safely

## Key Features

### Real Database Integration
- PostgreSQL 15 with full SQL support
- Database schema initialization
- Sample data population
- Health checks and monitoring

### Comprehensive Testing
- Unit tests with real database
- Integration tests with TestContainers
- API endpoint testing
- Performance and concurrent testing
- Error handling validation

### Jenkins Integration
- Parameterized builds
- Multiple test modes
- Artifact collection
- Build history tracking
- Console output monitoring

## Monitoring and Debugging

### View Job Progress
- Go to the job page
- Click on the build number
- View "Console Output" for detailed execution logs

### Check Logs
- Use "Console Output" for full build log
- Look for TestContainers container startup messages
- Monitor database initialization and test execution

### View Reports
- **Test Results**: JUnit test reports (if configured)
- **Artifacts**: Any generated test artifacts
- **Build History**: Track all job executions

### Troubleshooting
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

## Local Testing

### Run TestContainers Demo
```bash
cd Jenkins/jenkins-scenarios/scenario_02_testcontainers
python3 demo_testcontainers.py
```

### Run Tests
```bash
# TestContainers integration tests
python3 -m pytest tests/test_testcontainers_integration.py -v

# Application tests
python3 -m pytest tests/test_app.py -v

# All tests
python3 -m pytest tests/ -v
```

### Docker Compose Testing
```bash
docker-compose -f docker-compose.test.yml up --build
```

## Advanced Configuration

### Environment Variables
Configure these in Jenkins → Manage Jenkins → Configure System → Global Properties:

- `DB_TYPE`: Database type (testcontainers, postgresql)
- `TEST_MODE`: Test mode to run (demo, tests, app-tests, docker, all)
- `DOCKER_REGISTRY`: Your Docker registry URL (optional)

### Credentials Setup
1. **Jenkins → Manage Jenkins → Manage Credentials**
2. **Add credentials for**:
   - Docker registry login (if pushing images)
   - GitHub access (if using private repos)

## Learning Objectives

After completing this scenario, you will understand:

- How to integrate TestContainers with Jenkins
- Real database testing vs. mocking
- Container-based integration testing patterns
- Jenkins job configuration for complex testing
- PostgreSQL integration in CI/CD pipelines
- Performance testing with real databases

## Next Steps

- Explore other TestContainers scenarios
- Try different database types (MySQL, MongoDB, Redis)
- Integrate with your own applications
- Learn about TestContainers for other languages
- Study container orchestration patterns

## Resources

- [TestContainers Documentation](https://testcontainers.org/)
- [TestContainers Python](https://testcontainers-python.readthedocs.io/)
- [Jenkins Testing Guide](https://jenkins.io/doc/book/pipeline/testing/)
- [Docker Testing Patterns](https://docs.docker.com/develop/dev-best-practices/)