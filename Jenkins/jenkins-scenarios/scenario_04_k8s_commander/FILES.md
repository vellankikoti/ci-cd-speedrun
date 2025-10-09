# 📁 Scenario 04: File Structure

This document explains what each file does and which ones are essential.

---

## 📋 Core Files (Required)

### `Jenkinsfile` (82KB)
**Purpose**: Main pipeline definition with embedded Python web application

**What it does**:
- Defines Jenkins pipeline parameters
- Builds Docker container with Python web app
- Deploys interactive K8s Commander learning platform
- Handles port binding with automatic retry logic

**For attendees**: This is the heart of the scenario. Jenkins reads this file to run the pipeline.

---

### `README.md` (11KB)
**Purpose**: Comprehensive documentation

**Contents**:
- What is K8s Commander
- Features and learning outcomes
- Detailed setup instructions
- API endpoints documentation
- Troubleshooting guide
- Production patterns with YAML examples

**For attendees**: Read this for complete understanding of the scenario.

---

### `QUICKSTART.md` (4.2KB)
**Purpose**: 5-minute getting started guide

**Contents**:
- 3-step setup process
- Parameter explanations
- Quick troubleshooting
- What to explore in the app

**For attendees**: Start here! Get running in 5 minutes, then read README for depth.

---

## 🛠️ Utility Scripts (Optional but Useful)

### `cleanup.py` (5.3KB)
**Purpose**: Clean up Docker containers and resources

**Usage**:
```bash
python3 cleanup.py
```

**What it does**:
- Stops and removes k8s-commander containers
- Frees up ports
- Cleans up Docker images

**For attendees**: Run this between builds to clean up.

---

### `verify-fix.sh` (5.4KB)
**Purpose**: Verify deployment and test functionality

**Usage**:
```bash
BUILD_NUMBER=38 ./verify-fix.sh
```

**What it does**:
- Checks if container is running
- Verifies port mappings
- Tests API endpoints
- Shows port conflicts

**For attendees**: Use this to debug deployment issues.

---

### `.gitignore` (246B)
**Purpose**: Prevent generated files from being committed

**What it ignores**:
- Generated Dockerfile
- k8s-demo/ and k8s-lab/ directories
- Port files and logs
- IDE configurations

**For attendees**: Keeps your git repo clean when you fork/modify.

---

## 📊 File Summary

| File | Size | Essential? | Purpose |
|------|------|------------|---------|
| `Jenkinsfile` | 82KB | ✅ Yes | Pipeline definition |
| `README.md` | 11KB | ✅ Yes | Full documentation |
| `QUICKSTART.md` | 4.2KB | ✅ Yes | Quick start guide |
| `cleanup.py` | 5.3KB | 🔧 Utility | Cleanup containers |
| `verify-fix.sh` | 5.4KB | 🔧 Utility | Verify deployment |
| `.gitignore` | 246B | 📝 Config | Git ignore rules |

---

## 🗂️ Generated Files (During Pipeline Execution)

These files are created when you run the pipeline and are **not committed to git**:

### `Dockerfile`
- Generated dynamically by Jenkinsfile
- Contains Python web application code
- Configured with environment variables

### `webapp.port`
- Contains the external port number
- Used to track which port was assigned

### `k8s-demo/`
- Sample Kubernetes YAML files
- Pod, Service, Deployment examples
- Generated based on selected K8S_CONCEPT

### `k8s-lab/`
- Hands-on lab instructions
- kubectl command exercises
- Practice scenarios

---

## 🎯 For Workshop Attendees

### Minimum Required Files
You only need these 3 files to run the scenario:
1. ✅ `Jenkinsfile`
2. ✅ `README.md` or `QUICKSTART.md`
3. ✅ Git repository access

### Recommended Files
Include these for better experience:
- 🔧 `cleanup.py` - Clean up between runs
- 🔧 `verify-fix.sh` - Debug issues
- 📝 `.gitignore` - Keep git clean

### Nice to Have
- 📚 `FILES.md` (this file) - Understand structure
- 📖 Full `README.md` - Deep dive

---

## 🧹 Cleanup

To remove all generated files:

```bash
# Manual cleanup
rm -rf k8s-demo/ k8s-lab/ Dockerfile webapp.port

# Or use the cleanup script
python3 cleanup.py

# Stop containers
docker ps -a --filter "name=k8s-commander" --format "{{.Names}}" | xargs docker rm -f
```

---

## 📦 Directory Structure

```
scenario_04_k8s_commander/
├── Jenkinsfile              # ✅ Pipeline definition
├── README.md                # ✅ Full documentation
├── QUICKSTART.md            # ✅ Quick start guide
├── cleanup.py               # 🔧 Cleanup utility
├── verify-fix.sh            # 🔧 Verification utility
├── .gitignore               # 📝 Git ignore rules
├── FILES.md                 # 📚 This file
│
└── Generated during runtime:
    ├── Dockerfile           # 🔄 Dynamic
    ├── webapp.port          # 🔄 Dynamic
    ├── k8s-demo/            # 🔄 Dynamic
    └── k8s-lab/             # 🔄 Dynamic
```

---

## 🎓 For Instructors

**Distributing to attendees**:
1. Share the Git repository URL
2. Point them to `QUICKSTART.md`
3. Have `cleanup.py` ready for troubleshooting
4. Keep `verify-fix.sh` handy for debugging

**Workshop prep checklist**:
- [ ] Test Jenkinsfile with all parameter combinations
- [ ] Verify QUICKSTART.md instructions are accurate
- [ ] Ensure Docker and Jenkins are running
- [ ] Have cleanup.py ready for quick resets
- [ ] Test with ports 8081-8131 availability

---

## 📞 Support

For questions about any file:
- Check README.md for detailed explanations
- Check QUICKSTART.md for quick answers
- Run verify-fix.sh for diagnostic information
- Run cleanup.py if things get messy

---

**Everything you need, nothing you don't.** 🎯
