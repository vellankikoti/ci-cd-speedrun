# 🚀 Jenkins Quick Reference Card

## ⚡ 5-Minute Setup

### 1. Create Job
```
Dashboard → New Item → chaos-ci-pipeline → Pipeline → OK
```

### 2. Configure Parameters
```
General Tab → ✅ This project is parameterized
Add Parameter:
- Name: SCENARIO
- Type: Choice Parameter
- Choices:
  chaos-full
  chaos-1
  chaos-2
  chaos-3
  chaos-free
  progressive-demo
- Default: progressive-demo
```

### 3. Configure Pipeline
```
Pipeline Tab → Definition: Pipeline script from SCM
SCM: Git
Repository URL: https://github.com/your-username/your-repo.git
Branch Specifier: */main
Script Path: Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile
```

### 4. Save & Test
```
Save → Build with Parameters → Select progressive-demo → Build
```

## 🔧 Common Issues & Fixes

| Issue | Quick Fix |
|-------|-----------|
| "Script not found" | Check Script Path spelling |
| "No parameters" | Verify "This project is parameterized" is checked |
| "Git credentials" | Add credentials in Manage Jenkins > Credentials |
| "Branch not found" | Change Branch Specifier to match your repo |
| "Docker not found" | Install Docker plugin in Jenkins |

## 🎯 Expected Workflow

1. **Setup** (5 minutes)
   - Create job with parameters
   - Configure pipeline script
   - Save configuration

2. **First Run** (2 minutes)
   - Click "Build with Parameters"
   - Select `progressive-demo`
   - Click "Build"

3. **Watch Chaos** (10 minutes)
   - Monitor real-time logs
   - See educational messages
   - Watch progressive failures
   - Celebrate success! 🎉

## 📋 Verification Checklist

- [ ] Job name: `chaos-ci-pipeline`
- [ ] Parameter: `SCENARIO` (Choice Parameter)
- [ ] Script Path: `Docker/docker-scenarios/scenario_02_chaos_pipeline/pipeline/Jenkinsfile`
- [ ] Repository URL: Your actual repo URL
- [ ] Branch: `*/main` or `*/master`
- [ ] "Build with Parameters" button visible
- [ ] Build starts without errors

## 🎓 What You'll See

### Simplified Mode (No Files)
```
🔄 Running simplified chaos scenario
🔥 CHAOS FULL: Unleashing maximum chaos!
💥 Chaos scenario completed!
```

### Full Mode (With Files)
```
🎓 Running complete progressive chaos demo
🧪 Testing individual steps...
🏭 Testing Step 5 production system...
📊 Analyzing chaos scenario results...
🎉 Success! Chaos scenario completed successfully.
```

## 🚨 Troubleshooting

### Immediate Failures
1. **"Script not found"** → Check Script Path
2. **"No parameters"** → Check "This project is parameterized"
3. **"Git error"** → Add credentials or check URL
4. **"Docker not found"** → Install Docker plugin

### Build Failures
1. **Port conflicts** → Ensure ports 8081-8085 are free
2. **Permission denied** → Check Jenkins user permissions
3. **Memory issues** → Increase Jenkins memory allocation

## 📞 Need Help?

1. Check the full [JENKINS_SETUP.md](JENKINS_SETUP.md) guide
2. Review the [troubleshooting section](JENKINS_SETUP.md#troubleshooting)
3. Verify your setup with the [verification checklist](JENKINS_SETUP.md#verification-checklist)

---

**Happy Chaos Engineering! 🎭** 