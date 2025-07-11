# 🛠️ Scenario 2: Security Troubleshooting Guide

**"Even Security Heroes Need Debugging Sometimes!" 🦸‍♂️🔐**

---

## 🚨 **QUICK EMERGENCY RESET**

If everything is broken and you need to start fresh:

```bash
# Nuclear option - delete everything and start over
kubectl delete namespace secure-todo --force --grace-period=0

# Wait 30 seconds, then re-run
sleep 30
python3 hero-solution/deploy-secure-todo.py
```

---

## 🔍 **SECURITY-SPECIFIC TROUBLESHOOTING**

### **Issue 1: "Secret not found" errors**

**Symptoms**: 
```
Error: secret "mysql-credentials" not found
Pod status: CreateContainerConfigError
```

**Root Cause**: Secrets not created before deployments

**Solutions**:

```bash
# Step 1: Check if secrets exist
kubectl get secrets -n secure-todo

# Step 2: If secrets missing, recreate them
python3 hero-solution/deploy-secure-todo.py

# Step 3: Verify secret contents (without exposing values)
kubectl describe secret mysql-credentials -n secure-todo
kubectl describe secret app-credentials -n secure-todo

# Step 4: Check secret has correct keys
kubectl get secret mysql-credentials -n secure-todo -o yaml
```

**Prevention**:
```python
# Always create secrets before deployments in the Python script
def deploy_everything(self):
    self.create_namespace()
    self.create_mysql_secrets()    # BEFORE deployments
    self.create_app_secrets()      # BEFORE deployments  
    self.deploy_secure_mysql()     # AFTER secrets
    self.deploy_secure_todo_app()  # AFTER secrets
```

---

### **Issue 2: MySQL container keeps crashing**

**Symptoms**:
```
kubectl get pods -n secure-todo
# secure-mysql-xxx   0/1   CrashLoopBackOff   0   2m
```

**Diagnosis**:
```bash
# Check pod events
kubectl describe pod -n secure-todo -l app=secure-mysql

# Check container logs
kubectl logs -n secure-todo -l app=secure-mysql

# Common error messages:
# "Access denied for user 'root'@'localhost'"
# "Can't connect to local MySQL server"
# "mysqld: Can't create/write to file"
```

**Solutions**:

#### **For Password Issues:**
```bash
# Check if secret has correct password format
kubectl get secret mysql-credentials -n secure-todo -o jsonpath='{.data.mysql-root-password}' | base64 -d
# Should show a strong password, not empty or malformed

# Recreate secrets with fresh passwords
python3 hero-solution/rotate-secrets.py
```

#### **For Permission Issues:**
```bash
# MySQL container needs write access
# Check if security context is too restrictive
kubectl get deployment secure-mysql -n secure-todo -o yaml | grep -A 10 securityContext

# Fix: Update security context in deployment
```

#### **For Resource Issues:**
```bash
# Check if MySQL has enough resources
kubectl top pod -n secure-todo
kubectl describe node | grep -A 5 "Allocated resources"

# Increase MySQL resources if needed
```

---

### **Issue 3: Todo app can't connect to database**

**Symptoms**:
```
kubectl logs -n secure-todo -l app=secure-todo-app
# Error: "Can't connect to MySQL server on 'secure-mysql-service'"
# Error: "Access denied for user 'todoapp_user'@'%'"
```

**Diagnosis**:
```bash
# Step 1: Check if MySQL service exists and is accessible
kubectl get svc -n secure-todo
kubectl describe svc secure-mysql-service -n secure-todo

# Step 2: Check if MySQL pods are ready
kubectl get pods -n secure-todo -l app=secure-mysql

# Step 3: Test database connectivity from todo app pod
kubectl exec -n secure-todo deployment/secure-todo-app -- nc -zv secure-mysql-service 3306
```

**Solutions**:

#### **For Service Discovery Issues:**
```bash
# Check DNS resolution
kubectl exec -n secure-todo deployment/secure-todo-app -- nslookup secure-mysql-service

# Check service endpoints
kubectl get endpoints -n secure-todo

# If no endpoints, MySQL pods are not ready
kubectl describe pod -n secure-todo -l app=secure-mysql
```

#### **For Authentication Issues:**
```bash
# Verify database credentials match between secrets
kubectl get secret mysql-credentials -n secure-todo -o yaml

# Check if todo app is using correct secret references
kubectl describe deployment secure-todo-app -n secure-todo | grep -A 20 "Environment"

# Test database login manually
kubectl exec -n secure-todo deployment/secure-mysql -- mysql -u root -p$(kubectl get secret mysql-credentials -n secure-todo -o jsonpath='{.data.mysql-root-password}' | base64 -d) -e "SHOW DATABASES;"
```

---

### **Issue 4: "Permission denied" accessing todo app**

**Symptoms**:
- Can't access todo app at http://localhost:31001
- Service exists but connection refused

**Solutions by Environment**:

#### **Docker Desktop:**
```bash
# Check if service port is accessible
kubectl get svc secure-todo-service -n secure-todo

# Try port forwarding (universal solution)
kubectl port-forward svc/secure-todo-service -n secure-todo 31501:80
# Access: http://localhost:31501
```

#### **Minikube:**
```bash
# Get Minikube IP
minikube ip

# Access using Minikube IP
open http://$(minikube ip):31001

# Or use minikube service command
minikube service secure-todo-service -n secure-todo
```

#### **EKS/Cloud:**
```bash
# Get node external IPs
kubectl get nodes -o wide

# Use any External-IP with port 31001
# Example: http://3.15.24.76:31001
```

---

### **Issue 5: Secret rotation fails**

**Symptoms**:
```bash
python3 hero-solution/rotate-secrets.py
# Error: "Failed to update secret mysql-credentials"
# Error: "Deployment restart failed"
```

**Diagnosis**:
```bash
# Check current secret status
kubectl describe secret mysql-credentials -n secure-todo
kubectl describe secret app-credentials -n secure-todo

# Check RBAC permissions
kubectl auth can-i update secrets --namespace secure-todo
kubectl auth can-i patch deployments --namespace secure-todo
```

**Solutions**:

#### **For Permission Issues:**
```bash
# Grant necessary RBAC permissions
kubectl create clusterrolebinding workshop-admin \
  --clusterrole=cluster-admin \
  --user=$(kubectl config view --minify -o jsonpath='{.contexts[0].context.user}')
```

#### **For Secret Update Issues:**
```bash
# Manual secret rotation
kubectl delete secret mysql-credentials -n secure-todo
kubectl delete secret app-credentials -n secure-todo

# Recreate with new values
python3 hero-solution/deploy-secure-todo.py
```

#### **For Deployment Restart Issues:**
```bash
# Manual deployment restart
kubectl rollout restart deployment/secure-mysql -n secure-todo
kubectl rollout restart deployment/secure-todo-app -n secure-todo

# Check rollout status
kubectl rollout status deployment/secure-mysql -n secure-todo
kubectl rollout status deployment/secure-todo-app -n secure-todo
```

---

### **Issue 6: Security monitoring shows failures**

**Symptoms**:
```bash
python3 hero-solution/security-monitor.py
# Shows: "❌ POOR" security status
# Shows: "⚠️ NEEDS ROTATION" for secrets
```

**Diagnosis**:
```bash
# Check specific security issues
kubectl describe deployment secure-mysql -n secure-todo | grep -A 10 securityContext
kubectl describe deployment secure-todo-app -n secure-todo | grep -A 10 securityContext

# Check resource limits
kubectl describe deployment secure-mysql -n secure-todo | grep -A 5 "Limits\|Requests"
```

**Solutions**:

#### **For Missing Security Context:**
```bash
# Redeploy with proper security context
python3 hero-solution/deploy-secure-todo.py
```

#### **For Missing Resource Limits:**
```bash
# Check if resources are properly set
kubectl get deployment secure-mysql -n secure-todo -o yaml | grep -A 10 resources
```

#### **For Old Secrets:**
```bash
# Force secret rotation
python3 hero-solution/rotate-secrets.py
```

---

### **Issue 7: Python script dependencies fail**

**Symptoms**:
```
ModuleNotFoundError: No module named 'cryptography'
ImportError: cannot import name 'Fernet'
```

**Solutions**:

```bash
# Install missing security dependencies
pip3 install cryptography==41.0.7
pip3 install mysql-connector-python==8.2.0

# Or install all requirements
pip3 install -r hero-solution/requirements.txt

# If using virtual environment
source venv/bin/activate  # Linux/Mac
pip install -r hero-solution/requirements.txt
```

---

### **Issue 8: Database data persistence issues**

**Symptoms**:
- Todo items disappear after MySQL pod restart
- Database tables not created

**Root Cause**: Using emptyDir for database storage (demo limitation)

**Solutions**:

#### **For Demo Environment:**
```bash
# This is expected behavior with emptyDir
# Data is meant to be temporary for workshop

# To test persistence, avoid pod restarts during demo
```

#### **For Production Environment:**
```yaml
# Replace emptyDir with PersistentVolumeClaim
volumeMounts:
- name: mysql-storage
  mountPath: /var/lib/mysql
volumes:
- name: mysql-storage
  persistentVolumeClaim:
    claimName: mysql-pvc
```

---

### **Issue 9: Health check failures**

**Symptoms**:
```
kubectl get pods -n secure-todo
# secure-mysql-xxx   0/1   Running   3   5m
# Restart count keeps increasing
```

**Diagnosis**:
```bash
# Check health check configuration
kubectl describe pod -n secure-todo -l app=secure-mysql | grep -A 10 "Liveness\|Readiness"

# Check health check logs
kubectl logs -n secure-todo -l app=secure-mysql --previous
```

**Solutions**:

#### **For MySQL Health Checks:**
```bash
# Test health check command manually
kubectl exec -n secure-todo deployment/secure-mysql -- mysqladmin ping -h localhost

# If fails, check MySQL startup time
kubectl describe pod -n secure-todo -l app=secure-mysql
```

#### **For Todo App Health Checks:**
```bash
# Test health endpoints
kubectl exec -n secure-todo deployment/secure-todo-app -- curl -f http://localhost:5000/

# If app doesn't have health endpoints, use basic connectivity
kubectl exec -n secure-todo deployment/secure-todo-app -- nc -z localhost 5000
```

---

### **Issue 10: Network connectivity problems**

**Symptoms**:
- Pods can't reach each other
- DNS resolution fails
- Network timeouts

**Diagnosis**:
```bash
# Check DNS resolution
kubectl exec -n secure-todo deployment/secure-todo-app -- nslookup secure-mysql-service

# Check network policies (if any)
kubectl get networkpolicies -n secure-todo

# Test basic connectivity
kubectl exec -n secure-todo deployment/secure-todo-app -- ping secure-mysql-service
```

**Solutions**:

#### **For DNS Issues:**
```bash
# Check CoreDNS status
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Restart CoreDNS if needed
kubectl rollout restart deployment/coredns -n kube-system
```

#### **For Network Policy Issues:**
```bash
# Check if network policies are blocking traffic
kubectl describe networkpolicy -n secure-todo

# Temporarily remove network policies for testing
kubectl delete networkpolicy --all -n secure-todo
```

---

## 📞 **GETTING HELP**

### **Step-by-Step Security Debugging:**

1. **Check Security Status** 🔍
   ```bash
   python3 hero-solution/security-monitor.py
   ```

2. **Verify Basic Connectivity** 🔗
   ```bash
   kubectl get all -n secure-todo
   kubectl get secrets -n secure-todo
   ```

3. **Test Database Connection** 🗄️
   ```bash
   kubectl exec -n secure-todo deployment/secure-mysql -- mysql -u root -p -e "SHOW DATABASES;"
   ```

4. **Check Application Logs** 📝
   ```bash
   kubectl logs -n secure-todo -l app=secure-todo-app
   kubectl logs -n secure-todo -l app=secure-mysql
   ```

5. **Try Nuclear Reset** 💥
   ```bash
   kubectl delete namespace secure-todo
   python3 hero-solution/deploy-secure-todo.py
   ```

### **When to Ask for Help:**

- ✅ **After trying the above steps**
- ✅ **With specific error messages**
- ✅ **With your environment details** (Docker Desktop/Minikube/EKS)
- ✅ **With output from security monitoring**

### **What to Include When Asking:**

```bash
# Run this security info-gathering script:
echo "=== SECURITY ENVIRONMENT INFO ==="
kubectl version --client
python3 --version
pip3 list | grep -E "(kubernetes|cryptography|mysql)"

echo "=== SECURE TODO STATUS ==="
kubectl get all -n secure-todo
kubectl get secrets -n secure-todo
kubectl get events -n secure-todo --sort-by='.lastTimestamp'

echo "=== SECURITY MONITORING ==="
python3 hero-solution/security-monitor.py 2>&1 | head -20

echo "=== RECENT ERRORS ==="
kubectl logs -n secure-todo -l app=secure-mysql --tail=20
kubectl logs -n secure-todo -l app=secure-todo-app --tail=20
```

---

## 🎯 **SUCCESS VALIDATION**

### **How to Know Security is Working:**

✅ **Secret Success Indicators:**
```bash
# All secrets exist with proper metadata
kubectl get secrets -n secure-todo
kubectl describe secret mysql-credentials -n secure-todo | grep "rotation-policy"

# Security monitoring shows green status
python3 hero-solution/security-monitor.py
# Should show: "🛡️ EXCELLENT - All security controls are compliant"
```

✅ **Application Success Indicators:**
- Todo app loads in browser
- Can add, edit, and delete todo items
- Database connection working
- No container restarts due to crashes

✅ **Security Success Indicators:**
```bash
# No privileged containers
kubectl get pods -n secure-todo -o jsonpath='{.items[*].spec.securityContext.privileged}'
# Should be empty or "false"

# Database not externally accessible
kubectl get svc -n secure-todo
# secure-mysql-service should be ClusterIP, not NodePort/LoadBalancer

# Secrets properly referenced, not hardcoded
kubectl get deployment secure-todo-app -n secure-todo -o yaml | grep -A 5 secretKeyRef
# Should show secret references, not plain text values
```

---

## 🔐 **SECURITY BEST PRACTICES CHECKLIST**

### **During Troubleshooting:**

- [ ] ✅ **Never log secret values** - Use `kubectl describe` not `kubectl get -o yaml`
- [ ] ✅ **Don't expose secrets in debug output** - Mask sensitive information
- [ ] ✅ **Use port forwarding for access** - Avoid exposing services externally
- [ ] ✅ **Check security context** - Ensure non-root execution
- [ ] ✅ **Verify resource limits** - Prevent resource exhaustion
- [ ] ✅ **Monitor for security violations** - Use security monitoring tool

### **Common Security Mistakes to Avoid:**

❌ **Don't do this:**
```bash
# NEVER expose secret values in logs
kubectl get secret mysql-credentials -n secure-todo -o yaml
echo "Password is: $(kubectl get secret mysql-credentials -n secure-todo -o jsonpath='{.data.mysql-root-password}' | base64 -d)"
```

✅ **Do this instead:**
```bash
# Check secret existence without exposing values
kubectl describe secret mysql-credentials -n secure-todo
kubectl get secret mysql-credentials -n secure-todo -o jsonpath='{.metadata.name}'
```

❌ **Don't do this:**
```bash
# NEVER expose database externally for debugging
kubectl patch svc secure-mysql-service -n secure-todo -p '{"spec":{"type":"NodePort"}}'
```

✅ **Do this instead:**
```bash
# Use port forwarding for database access
kubectl port-forward svc/secure-mysql-service -n secure-todo 3306:3306
mysql -h 127.0.0.1 -P 3306 -u root -p
```

---

## 🚨 **EMERGENCY SECURITY PROCEDURES**

### **If Secrets Are Compromised:**

```bash
# 1. Immediately rotate all secrets
python3 hero-solution/rotate-secrets.py

# 2. Check for unauthorized access
kubectl get events -n secure-todo --sort-by='.lastTimestamp'
kubectl logs -n secure-todo -l app=secure-mysql | grep -i "access denied\|failed login"

# 3. Review security monitoring
python3 hero-solution/security-monitor.py

# 4. If needed, redeploy everything with new secrets
kubectl delete namespace secure-todo
python3 hero-solution/deploy-secure-todo.py
```

### **If Container Security is Breached:**

```bash
# 1. Check for privilege escalation
kubectl get pods -n secure-todo -o jsonpath='{.items[*].spec.securityContext}'

# 2. Check for unauthorized containers
kubectl get pods -n secure-todo
kubectl describe pods -n secure-todo | grep -A 5 "Image:"

# 3. Check for suspicious activities
kubectl logs -n secure-todo --all-containers=true | grep -i "error\|warning\|failed"

# 4. If compromised, redeploy immediately
kubectl delete namespace secure-todo --force --grace-period=0
python3 hero-solution/deploy-secure-todo.py
```

---

## 📊 **MONITORING AND ALERTING**

### **Continuous Security Monitoring:**

```bash
# Run continuous security monitoring
python3 hero-solution/security-monitor.py
# Choose option 2 for continuous monitoring

# Watch for security events
kubectl get events -n secure-todo --watch

# Monitor resource usage for anomalies
kubectl top pods -n secure-todo --watch
```

### **Security Metrics to Track:**

- **Secret Age**: Should rotate every 30 days (database) / 7 days (app)
- **Failed Login Attempts**: Should be minimal
- **Resource Usage**: Should stay within limits
- **Container Restarts**: Should be rare
- **Security Context Violations**: Should be zero

---

## 🏆 **REMEMBER: SECURITY IS A JOURNEY!**

**Even Security Heroes Face Challenges!** 

- Kubernetes security is complex - debugging is normal ✅
- Every security issue is a learning opportunity ✅  
- Automation prevents most security problems ✅
- The Chaos Agent teaches us to be better defenders! 🦸‍♂️

**Security Debugging Philosophy:**
*"Trust, but verify. Then verify again!"* 🛡️

**When in doubt**: 
1. Check the security monitoring first
2. Verify secrets are properly configured
3. Ensure network isolation is working
4. Delete and redeploy if needed
5. Learn from each security challenge

**Key Security Mantras:**
- 🔐 **"No hardcoded secrets, ever!"**
- 🛡️ **"Defense in depth, always!"**  
- 🔄 **"Rotate early, rotate often!"**
- 👁️ **"Monitor everything, trust nothing!"**
- 🚀 **"Automate security, don't hope for it!"**