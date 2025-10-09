# 🌍 Multi-Environment Deployment
**5 Minutes - The DevOps Professional's Environment Strategy**

*"In production, you don't deploy to production. You deploy to dev, then staging, then production. Each environment is a stepping stone to success."*

## 🎯 **The Professional's Challenge**

**Real-world scenario:** You're managing a microservices architecture with:
- 🏠 **Development** - 5 developers, 50 deployments/day
- 🧪 **Staging** - Production-like testing, 10 deployments/day  
- 🚀 **Production** - 10,000+ users, 1 deployment/day (when it's perfect)

**The problem:** Each environment needs different configurations, but you can't maintain 3 separate pipelines.

**Your mission:** Build one pipeline that adapts to any environment like a chameleon.

## 🚀 **Quick Start (30 seconds)**

```bash
# 1. Create Parameterized Pipeline Job
# New Item → Pipeline → Name: "multi-environment-deployment"
# Pipeline script from SCM → Git
# Repository: https://github.com/vellankikoti/ci-cd-chaos-workshop.git
# Branch: */docker-test
# Script Path: Jenkins/jenkins-scenarios/scenario_02_multi_environment/Jenkinsfile

# 2. Run with Parameters
# Click "Build with Parameters"
# Select Environment: staging
# Click "Build"
```

## 🎪 **The 5-Minute Masterclass**

### **Minute 1: The Parameter Strategy** ⏱️
**What you'll learn:** One pipeline, infinite environments

```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Target deployment environment'
        )
        choice(
            name: 'DEPLOYMENT_STRATEGY',
            choices: ['rolling', 'blue-green', 'canary'],
            description: 'Deployment strategy for this environment'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run automated tests'
        )
        choice(
            name: 'NOTIFICATION_CHANNEL',
            choices: ['slack', 'email', 'teams', 'none'],
            description: 'Notification channel for this deployment'
        )
    }
}
```

**💡 Pro Tip:** "Parameters are your environment chameleon. One pipeline, infinite possibilities."

### **Minute 2: Environment-Specific Configuration** ⏱️
**What you'll learn:** Configuration management that scales

```groovy
stage('🔧 Environment Configuration') {
    steps {
        script {
            // Environment-specific configurations
            def configs = [
                'dev': [
                    replicas: 1,
                    resources: 'small',
                    database: 'dev-db',
                    monitoring: 'basic',
                    backup: false
                ],
                'staging': [
                    replicas: 2,
                    resources: 'medium', 
                    database: 'staging-db',
                    monitoring: 'enhanced',
                    backup: true
                ],
                'production': [
                    replicas: 5,
                    resources: 'large',
                    database: 'prod-db',
                    monitoring: 'full',
                    backup: true
                ]
            ]
            
            def envConfig = configs[params.ENVIRONMENT]
            echo "🔧 Configuring for ${params.ENVIRONMENT}:"
            echo "  • Replicas: ${envConfig.replicas}"
            echo "  • Resources: ${envConfig.resources}"
            echo "  • Database: ${envConfig.database}"
            echo "  • Monitoring: ${envConfig.monitoring}"
        }
    }
}
```

**💡 Pro Tip:** "Configuration as code. No more environment-specific scripts scattered everywhere."

### **Minute 3: Conditional Testing Strategy** ⏱️
**What you'll learn:** Test what matters, when it matters

```groovy
stage('🧪 Environment-Specific Testing') {
    when {
        expression { params.RUN_TESTS == true }
    }
    steps {
        script {
            switch(params.ENVIRONMENT) {
                case 'dev':
                    echo "🧪 Development Testing:"
                    echo "  • Unit tests only"
                    echo "  • Quick smoke tests"
                    echo "  • No performance testing"
                    break
                case 'staging':
                    echo "🧪 Staging Testing:"
                    echo "  • Full test suite"
                    echo "  • Integration tests"
                    echo "  • Performance testing"
                    echo "  • Security scanning"
                    break
                case 'production':
                    echo "🧪 Production Testing:"
                    echo "  • Full test suite"
                    echo "  • Load testing"
                    echo "  • Security audit"
                    echo "  • Compliance checks"
                    break
            }
        }
    }
}
```

**💡 Pro Tip:** "Don't waste time running production tests in dev. Each environment has its purpose."

### **Minute 4: Smart Deployment Strategy** ⏱️
**What you'll learn:** Deploy like a pro, every time

```groovy
stage('🚀 Smart Deployment') {
    steps {
        script {
            def deploymentStrategy = params.DEPLOYMENT_STRATEGY
            
            switch(deploymentStrategy) {
                case 'rolling':
                    echo "🔄 Rolling Deployment:"
                    echo "  • Zero downtime"
                    echo "  • Gradual rollout"
                    echo "  • Automatic rollback on failure"
                    break
                case 'blue-green':
                    echo "🔵🟢 Blue-Green Deployment:"
                    echo "  • Instant switchover"
                    echo "  • Full testing before switch"
                    echo "  • Quick rollback capability"
                    break
                case 'canary':
                    echo "🐦 Canary Deployment:"
                    echo "  • 5% traffic to new version"
                    echo "  • Gradual increase based on metrics"
                    echo "  • Automatic rollback on issues"
                    break
            }
            
            // Environment-specific deployment
            switch(params.ENVIRONMENT) {
                case 'dev':
                    echo "🏠 Deploying to Development:"
                    echo "  • Single instance"
                    echo "  • Basic monitoring"
                    echo "  • Auto-deploy on commit"
                    break
                case 'staging':
                    echo "🧪 Deploying to Staging:"
                    echo "  • Production-like setup"
                    echo "  • Full monitoring"
                    echo "  • Manual approval required"
                    break
                case 'production':
                    echo "🚀 Deploying to Production:"
                    echo "  • High availability setup"
                    echo "  • Full monitoring + alerting"
                    echo "  • Multiple approvals required"
                    break
            }
        }
    }
}
```

**💡 Pro Tip:** "Different environments, different strategies. Dev needs speed, production needs safety."

### **Minute 5: Smart Notifications** ⏱️
**What you'll learn:** Notify the right people, at the right time

```groovy
stage('📢 Smart Notifications') {
    steps {
        script {
            def channel = params.NOTIFICATION_CHANNEL
            def environment = params.ENVIRONMENT
            
            switch(channel) {
                case 'slack':
                    echo "💬 Slack Notification:"
                    echo "  • Channel: #deployments-${environment}"
                    echo "  • Rich formatting with build status"
                    echo "  • Direct links to logs and dashboards"
                    break
                case 'email':
                    echo "📧 Email Notification:"
                    echo "  • To: devops-team@company.com"
                    echo "  • CC: ${environment}-team@company.com"
                    echo "  • Detailed deployment report"
                    break
                case 'teams':
                    echo "📱 Teams Notification:"
                    echo "  • Channel: ${environment}-deployments"
                    echo "  • Interactive cards with status"
                    echo "  • One-click access to monitoring"
                    break
            }
            
            // Environment-specific notification content
            switch(environment) {
                case 'dev':
                    echo "  • Notify: Development team only"
                    echo "  • Content: Quick status update"
                    break
                case 'staging':
                    echo "  • Notify: QA + DevOps teams"
                    echo "  • Content: Testing instructions"
                    break
                case 'production':
                    echo "  • Notify: Entire engineering team"
                    echo "  • Content: Full deployment report"
                    echo "  • Include: Performance metrics"
                    break
            }
        }
    }
}
```

**💡 Pro Tip:** "The right notification to the right people. Don't spam everyone with dev deployments."

## 🎯 **What Makes This Production-Grade?**

### **🌍 Multi-Environment Features:**
- ✅ **Parameterized builds** - One pipeline, all environments
- ✅ **Environment-specific configs** - No hardcoded values
- ✅ **Conditional testing** - Test what matters, when it matters
- ✅ **Smart deployment strategies** - Right strategy for each environment
- ✅ **Targeted notifications** - Right people, right time
- ✅ **Configuration as code** - Version controlled, auditable

### **📊 Environment Comparison:**
```
Development:
  • Deployments: 50/day
  • Testing: Basic
  • Monitoring: Minimal
  • Approval: None
  • Rollback: Automatic

Staging:
  • Deployments: 10/day
  • Testing: Full suite
  • Monitoring: Enhanced
  • Approval: Manual
  • Rollback: 2 minutes

Production:
  • Deployments: 1/day
  • Testing: Complete
  • Monitoring: Full
  • Approval: Multiple
  • Rollback: 30 seconds
```

## 🚨 **Real-World Production Scenarios**

### **Scenario A: The Hotfix Emergency**
*"Critical bug in production! Need to deploy fix immediately!"*

**What happens with this pipeline:**
1. **Select environment: production**
2. **Select strategy: blue-green** (safest)
3. **Skip tests: false** (always test in staging first)
4. **Notification: teams** (alert everyone)
5. **Result: Safe, fast, monitored deployment**

### **Scenario B: The Feature Rollout**
*"New feature ready for staging testing"*

**What happens with this pipeline:**
1. **Select environment: staging**
2. **Select strategy: rolling** (gradual)
3. **Run tests: true** (full validation)
4. **Notification: slack** (dev team only)
5. **Result: Thoroughly tested, ready for production**

## 🎓 **Key Learnings (5 Minutes)**

1. **🎛️ Parameters are powerful** - One pipeline, infinite environments
2. **🔧 Configuration as code** - No more environment-specific scripts
3. **🧪 Conditional testing** - Test what matters, when it matters
4. **🚀 Smart deployments** - Right strategy for each environment
5. **📢 Targeted notifications** - Right people, right time

## 🚀 **Next Level: Scenario 3**

*"Now that you can deploy anywhere, let's add security and compliance to protect your production systems..."*

---

**💬 The DevOps Professional's Wisdom:**
*"I've seen teams maintain 5 different pipelines for 5 environments. That's 5x the maintenance, 5x the bugs, 5x the headaches. One parameterized pipeline handles all environments. It's not just efficient - it's sanity."*

**Ready for the next challenge? Let's add security and compliance! 🛡️**
