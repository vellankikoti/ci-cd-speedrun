# 🔧 Jenkins SCM Setup Guide for Scenario 03

## 📋 Step-by-Step Jenkins Configuration

### **Step 1: Create New Jenkins Pipeline Job**

1. **In Jenkins Dashboard**, click **"New Item"**
2. **Enter item name**: `CI-CD-Chaos-Workshop-Scenario-03`
3. **Select**: **"Pipeline"** (the pipeline icon with the branching lines)
4. **Click**: **"OK"**

### **Step 2: Configure Pipeline Settings**

In the pipeline configuration page:

#### **General Section**
- ✅ **Description**: `Scenario 03: HTML Reports Chaos - Master test reporting under chaotic conditions`
- ✅ **Discard old builds**: Check this and set to keep 10 builds

#### **Build Triggers** (Optional)
- ✅ **GitHub hook trigger for GITScm polling** (if you want automatic builds)
- ✅ **Poll SCM**: `H/5 * * * *` (poll every 5 minutes)

#### **Pipeline Section** (This is the important part!)
- **Definition**: Select **"Pipeline script from SCM"**
- **SCM**: Select **"Git"**
- **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
- **Credentials**: Select appropriate credentials (or leave empty for public repo)
- **Branches to build**: `*/phase-3-jenkins`
- **Script Path**: `Jenkins/jenkins_scenarios/scenario_03_html_reports/Jenkinsfile`

#### **Advanced Options** (Click "Advanced" under Pipeline)
- **Lightweight checkout**: ✅ Check this for faster checkouts

### **Step 3: Save and Test**

1. **Click**: **"Save"**
2. **Click**: **"Build with Parameters"** (this should now be available)
3. **Set parameters**:
   - All scenarios: ✅ **ENABLED**
   - All modes: ✅ **PASS** (for first test)
4. **Click**: **"Build"**

## 🎯 Expected Repository Structure

Your GitHub repo should have this structure:

```
ci-cd-chaos-workshop/
├── Jenkins/
│   └── jenkins_scenarios/
│       └── scenario_03_html_reports/
│           ├── Jenkinsfile                    ← Pipeline script
│           ├── Dockerfile                     ← Container definition
│           ├── requirements.txt               ← Python dependencies
│           └── tests/                         ← Test files
│               ├── test_config_validation_pass.py
│               ├── test_config_validation_fail.py
│               ├── test_api_health_pass.py
│               ├── test_api_health_fail.py
│               ├── test_postgres_pass.py
│               ├── test_postgres_fail.py
│               ├── test_redis_pass.py
│               ├── test_redis_fail.py
│               ├── test_secret_scan_pass.py
│               └── test_secret_scan_fail.py
└── README.md
```

## 🔧 Updated Jenkinsfile Features

The updated Jenkinsfile now includes:

### **✅ SCM Integration**
- **Automatic checkout** from your GitHub repository
- **File verification** to ensure all required files exist
- **Branch-specific** configuration (`phase-3-jenkins`)

### **✅ Self-Contained Execution**
- **No manual file copying** required
- **All paths resolved** automatically from SCM
- **Git information** displayed in reports

### **✅ Enhanced Error Handling**
- **Pre-flight checks** for required files
- **Detailed error messages** if files are missing
- **Graceful failure handling** with educational messages

### **✅ Beautiful Reporting**
- **Git repository info** displayed in consolidated report
- **Build metadata** with timestamps
- **Enhanced visual design** with gradients and hover effects

## 🚀 Quick Test Commands

If you want to test locally before Jenkins:

```bash
# Clone your repo
git clone https://github.com/vellankikoti/ci-cd-chaos-workshop.git
cd ci-cd-chaos-workshop
git checkout phase-3-jenkins

# Navigate to scenario
cd Jenkins/jenkins_scenarios/scenario_03_html_reports

# Build Docker image
docker build -t scenario-03-test .

# Run a quick test
mkdir -p test-reports
docker run --rm \
  -v $(pwd)/test-reports:/app/reports \
  scenario-03-test \
  pytest tests/test_config_validation_pass.py \
    --html=reports/test.html \
    --self-contained-html \
    -v

# Check the report
open test-reports/test.html  # On Mac
# or
xdg-open test-reports/test.html  # On Linux
```

## 🔍 Troubleshooting

### **Issue: "Pipeline script from SCM" not visible**
- Make sure you selected **"Pipeline"** project type, not "Freestyle"
- The SCM option appears in the **Pipeline section** at the bottom of the config page

### **Issue: Repository not found**
- Verify the repository URL: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
- Check if the repository is public or if you need credentials
- Verify the branch exists: `phase-3-jenkins`

### **Issue: Script path not found**
- Verify the Jenkinsfile exists at: `Jenkins/jenkins_scenarios/scenario_03_html_reports/Jenkinsfile`
- Check file permissions and that it's committed to the branch

### **Issue: Docker permissions**
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Test Docker access
sudo -u jenkins docker ps
```

### **Issue: No test files found**
The pipeline will check for required files and show detailed error messages if anything is missing.

## 🎉 Success Indicators

You'll know everything is working when:

1. **✅ Build starts** with "Build with Parameters" button
2. **✅ Checkout stage** shows your repository URL and branch
3. **✅ Docker build** completes successfully  
4. **✅ Test stages** run (pass or fail as configured)
5. **✅ Reports generated** with beautiful HTML output
6. **✅ HTML Publisher** shows multiple report links

## 🎪 Ready to Go!

Once this is set up, you can:
- **Experiment** with different pass/fail combinations
- **Study** the beautiful HTML reports
- **Learn** from intentional failures
- **Share** your pipeline with team members
- **Extend** with additional scenarios

The pipeline is now **fully self-contained** and will pull everything from your GitHub repository automatically! 🚀