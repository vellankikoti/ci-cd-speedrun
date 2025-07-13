# Jenkins Setup Guide for Chaos Pipeline

This guide explains how to set up and run the chaos pipeline in Jenkins.

## 🚀 Quick Setup

### Option 1: Use the Setup Script (Recommended)

```bash
# Run the setup script to create all required files
./setup_jenkins_workspace.sh
```

This script will create:
- ✅ All scenario directories and files
- ✅ Pipeline scripts
- ✅ Demo scripts
- ✅ Docker compose configuration
- ✅ Proper permissions

### Option 2: Manual Setup

If you prefer to set up manually, ensure you have:

1. **Directory Structure:**
   ```
   scenario_02_chaos_pipeline/
   ├── scenarios/
   │   ├── step1_fail_network/
   │   ├── step2_fail_resource/
   │   ├── step3_fail_service/
   │   ├── step4_fail_db/
   │   └── step5_success/
   ├── pipeline/
   │   ├── Jenkinsfile
   │   └── chaos_scenarios.py
   ├── demo_manual.sh
   └── docker-compose-step5.yml
   ```

2. **Required Files:**
   - All scenario Dockerfiles and app.py files
   - Pipeline scripts
   - Demo scripts
   - Docker compose configuration

## 🔧 Jenkins Configuration

### 1. Create Jenkins Pipeline Job

1. Go to Jenkins Dashboard
2. Click "New Item"
3. Select "Pipeline"
4. Name it "chaos-ci-pipeline"

### 2. Configure Pipeline

In the pipeline configuration:

1. **Pipeline Definition:** Select "Pipeline script from SCM"
2. **SCM:** Select your version control system (Git)
3. **Repository URL:** Your repository URL
4. **Script Path:** `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`
5. **Branch Specifier:** `*/main` or `*/master` (depending on your default branch)
6. **Script Path:** `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`

**Detailed Steps:**

1. **In Jenkins Dashboard:**
   - Click "New Item" or "Create new jobs"
   - Enter job name: `chaos-ci-pipeline`
   - Select "Pipeline"
   - Click "OK"

2. **In Pipeline Configuration:**
   - **General Tab:**
     - ✅ Check "This project is parameterized"
     - Add parameter: Name: `SCENARIO`, Type: `Choice Parameter`
     - Choices:
       ```
       chaos-full
       chaos-1
       chaos-2
       chaos-3
       chaos-free
       progressive-demo
       ```
     - Default Value: `progressive-demo`
     - Description: `Select the chaos scenario to run`

   - **Pipeline Tab:**
     - **Definition:** Select "Pipeline script from SCM"
     - **SCM:** Select "Git"
     - **Repository URL:** `https://github.com/your-username/your-repo.git`
     - **Credentials:** Add your Git credentials if needed
     - **Branch Specifier:** `*/main` (or `*/master`)
     - **Script Path:** `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`

3. **Advanced Options (if needed):**
   - **Lightweight checkout:** ✅ Check this for faster builds
   - **Poll SCM:** Leave unchecked (or set schedule if you want automatic builds)

4. **Build Triggers:**
   - Leave unchecked for manual builds
   - Or configure as needed (GitHub webhooks, polling, etc.)

5. **Post-build Actions:**
   - Leave empty for now (pipeline handles cleanup)

6. **Click "Save"**

### 3. Build Parameters

The pipeline supports these parameters:

- **SCENARIO:** Select the chaos scenario to run
  - `chaos-full`: Maximum chaos (everything broken)
  - `chaos-1`: Network fixed, other issues remain
  - `chaos-2`: Resources fixed, service issues remain
  - `chaos-3`: Services fixed, database issues remain
  - `chaos-free`: Perfect pipeline (all working)
  - `progressive-demo`: Complete educational demo

## 🎯 Running the Pipeline

### Method 1: Jenkins Web Interface

1. **Navigate to your job:**
   - Go to Jenkins Dashboard
   - Find and click on your `chaos-ci-pipeline` job

2. **Start a build:**
   - Click "Build with Parameters" (blue button)
   - You should see a dropdown for "SCENARIO" parameter
   - Select your desired scenario (recommended: `progressive-demo`)
   - Click "Build" (blue button)

3. **Monitor the build:**
   - Click on the build number to see real-time logs
   - Watch the pipeline stages execute
   - Look for educational messages and chaos scenarios

**Expected workflow:**
```
Dashboard → chaos-ci-pipeline → Build with Parameters → 
Select SCENARIO → Build → Watch logs → See chaos unfold! 🎭
```

### Method 2: Command Line

```bash
# Trigger build with parameters
curl -X POST "http://your-jenkins-url/job/chaos-ci-pipeline/buildWithParameters" \
  --data-urlencode "SCENARIO=progressive-demo"
```

## ✅ Verification Checklist

Before running your first build, verify these items:

### 1. **Job Configuration**
- [ ] Job name is `chaos-ci-pipeline`
- [ ] Job type is "Pipeline"
- [ ] "This project is parameterized" is checked
- [ ] Parameter name is `SCENARIO`
- [ ] Parameter type is "Choice Parameter"
- [ ] All scenario choices are listed
- [ ] Default value is `progressive-demo`

### 2. **Pipeline Configuration**
- [ ] Definition is "Pipeline script from SCM"
- [ ] SCM is "Git"
- [ ] Repository URL is correct
- [ ] Credentials are configured (if needed)
- [ ] Branch specifier matches your repository
- [ ] Script path is `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`

### 3. **Repository Setup**
- [ ] Repository contains the scenario files
- [ ] Branch exists and is accessible
- [ ] Jenkinsfile exists at the specified path
- [ ] All required files are committed and pushed

### 4. **Jenkins Environment**
- [ ] Docker is available in Jenkins
- [ ] Jenkins has sufficient permissions
- [ ] Required ports (8081-8085) are available
- [ ] Jenkins can access the internet (for Docker images)

### 5. **Test Run**
- [ ] Job saves without errors
- [ ] "Build with Parameters" button is visible
- [ ] Parameter dropdown shows all options
- [ ] Build starts without immediate failures

**If any item is missing, refer to the troubleshooting section below.**

---

## 📊 Understanding Pipeline Output

If the workspace doesn't have the required files, the pipeline runs in "simplified mode":

```
🔄 Running simplified chaos scenario (no local files)
🔥 CHAOS FULL: Unleashing maximum chaos!
This scenario demonstrates multiple failure modes:
1. Network connectivity issues
2. Resource exhaustion
3. Service dependency failures
4. Database connection problems
```

### Full Mode

When all files are available, you'll see:

```
🎓 Running complete progressive chaos demo...
🧪 Testing individual steps...
🏭 Testing Step 5 production system with Redis and MySQL...
📊 Analyzing chaos scenario results...
```

## 🔍 Troubleshooting

### Common Issues

1. **"No such file or directory" errors**
   - Run `./setup_jenkins_workspace.sh` to create required files
   - Ensure your repository contains all scenario files

2. **Docker build failures**
   - Check that Docker is available in Jenkins
   - Verify Dockerfile syntax in each scenario

3. **Port conflicts**
   - The pipeline uses ports 8081-8085
   - Ensure these ports are available

4. **Permission denied errors**
   - Ensure scripts have execute permissions
   - Check Jenkins user permissions

5. **Pipeline script not found**
   - Verify the Script Path is correct: `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`
   - Check that the file exists in your repository
   - Ensure the branch specifier matches your repository's default branch

6. **Parameter not showing in build**
   - Make sure "This project is parameterized" is checked
   - Verify the parameter name is exactly `SCENARIO`
   - Check that the parameter type is "Choice Parameter"

7. **Git credentials issues**
   - Add your Git credentials in Jenkins (Manage Jenkins > Manage Credentials)
   - Use SSH keys or username/password as appropriate
   - Test the repository connection in the job configuration

8. **Branch not found**
   - Verify your repository has the correct default branch (main/master)
   - Update the Branch Specifier to match your repository
   - Check that the branch exists and contains the required files

### Debug Mode

To see more detailed output, modify the Jenkinsfile:

```groovy
// Add this to any stage for debugging
sh """
    echo "🔍 Debug information:"
    pwd
    ls -la
    docker ps
    docker images
"""
```

## 🎓 Educational Scenarios

### Progressive Demo (Recommended)

The `progressive-demo` scenario provides a complete educational experience:

1. **Step 1:** Network connectivity issues
2. **Step 2:** Resource management challenges
3. **Step 3:** Service dependency failures
4. **Step 4:** Database connectivity problems
5. **Step 5:** Production-ready system with Redis and MySQL

### Individual Scenarios

Each scenario focuses on specific failure modes:

- **chaos-full:** Everything broken (maximum chaos)
- **chaos-free:** Perfect pipeline (all working)
- **chaos-1/2/3:** Progressive fixes showing how issues cascade

## 📈 Monitoring and Analysis

The pipeline provides:

- **Real-time logs:** See each step as it executes
- **Container status:** Monitor Docker containers
- **Health checks:** Verify service endpoints
- **Resource usage:** Track memory and CPU usage
- **Educational insights:** Learn from each failure mode

## 🧹 Cleanup

The pipeline automatically cleans up:

- All chaos containers
- Test containers
- Docker compose services
- Temporary files

## 🎉 Success Indicators

A successful run will show:

```
🎉 Success! Chaos scenario completed successfully.
✅ All required files found
🎓 Complete educational journey through all chaos scenarios
🏭 Real production system with Redis and MySQL
```

## 📚 Additional Resources

- [Chaos Engineering Principles](https://principlesofchaos.org/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Happy Chaos Engineering! 🎭** 