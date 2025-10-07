# Jenkins EKS Pipeline Troubleshooting Guide

## 🚨 **Common Issues and Solutions**

### **Issue 1: "Could not find credentials entry with ID ''"**

**Error Message:**
```
ERROR: Could not find credentials entry with ID ''
```

**Cause:** The AWS_CREDENTIALS parameter is empty or not configured.

**Solution:**
1. **Create AWS Credentials in Jenkins:**
   - Go to Jenkins Dashboard → Manage Jenkins → Manage Credentials
   - Click "Add Credentials" → "Username with password"
   - Username: Your AWS Access Key ID (e.g., `AKIA...`)
   - Password: Your AWS Secret Access Key
   - ID: `aws-workshop-credentials` (or any name you prefer)
   - Description: "AWS credentials for EKS workshop"

2. **Re-run the Job with Parameters:**
   - Go to your Jenkins job
   - Click "Build with Parameters"
   - Select the credentials you created from the "AWS_CREDENTIALS" dropdown
   - Fill in other parameters:
     - CLUSTER_NAME: `my-workshop-cluster`
     - AWS_REGION: `us-west-2`
     - NODE_INSTANCE_TYPE: `t3.small`
     - NODE_COUNT: `3`
     - ENABLE_LOGGING: `true`
     - ENABLE_ALB_CONTROLLER: `true`
   - Click "Build"

### **Issue 2: "Access Denied" or "Invalid Credentials"**

**Error Message:**
```
Access Denied: User is not authorized to perform: eks:CreateCluster
```

**Cause:** AWS credentials don't have sufficient permissions.

**Solution:**
1. **Check AWS Permissions:**
   ```bash
   aws sts get-caller-identity
   ```

2. **Attach Required IAM Policy:**
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "eks:*",
                   "ec2:*",
                   "iam:*",
                   "cloudformation:*",
                   "sts:GetCallerIdentity"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

### **Issue 3: "Region not supported" or "Invalid region"**

**Error Message:**
```
Invalid region: us-east-1
```

**Cause:** The selected region doesn't support EKS or has different naming.

**Solution:**
1. **Check EKS-supported regions:**
   ```bash
   aws eks list-clusters --region us-west-2
   ```

2. **Use supported regions:**
   - `us-west-2` (Oregon) - Recommended
   - `us-east-1` (N. Virginia)
   - `us-east-2` (Ohio)
   - `eu-west-1` (Ireland)
   - `ap-southeast-1` (Singapore)

### **Issue 4: "Cluster already exists"**

**Error Message:**
```
Cluster already exists: my-workshop-cluster-1
```

**Cause:** A cluster with the same name already exists.

**Solution:**
1. **Delete existing cluster:**
   ```bash
   aws eks delete-cluster --name my-workshop-cluster-1 --region us-west-2
   ```

2. **Or use a different cluster name:**
   - Change CLUSTER_NAME parameter to something unique
   - e.g., `my-workshop-cluster-$(date +%s)`

### **Issue 5: "Insufficient EC2 capacity"**

**Error Message:**
```
Insufficient capacity in the requested Availability Zone
```

**Cause:** The selected region/AZ doesn't have available capacity for the instance type.

**Solution:**
1. **Try a different region:**
   - Change AWS_REGION to `us-west-2` or `us-east-1`

2. **Try a different instance type:**
   - Change NODE_INSTANCE_TYPE to `t3.medium` or `t3.large`

3. **Check capacity:**
   ```bash
   aws ec2 describe-availability-zones --region us-west-2
   ```

## 🔧 **Step-by-Step Fix for Current Issue**

### **Step 1: Create AWS Credentials**
1. Go to Jenkins Dashboard
2. Click "Manage Jenkins" → "Manage Credentials"
3. Click "Add Credentials"
4. Select "Username with password"
5. Fill in:
   - **Username**: `AKIA...` (your AWS Access Key ID)
   - **Password**: `...` (your AWS Secret Access Key)
   - **ID**: `aws-workshop-credentials`
   - **Description**: "AWS credentials for EKS workshop"
6. Click "OK"

### **Step 2: Re-run the Job**
1. Go to your Jenkins job: "03 EKS Deployment - Production"
2. Click "Build with Parameters"
3. Select the credentials you just created from the dropdown
4. Set other parameters:
   - CLUSTER_NAME: `my-workshop-cluster`
   - AWS_REGION: `us-west-2`
   - NODE_INSTANCE_TYPE: `t3.small`
   - NODE_COUNT: `3`
   - ENABLE_LOGGING: `true`
   - ENABLE_ALB_CONTROLLER: `true`
5. Click "Build"

### **Step 3: Monitor the Build**
1. Click on the build number to view progress
2. Check the "Configure AWS Credentials" stage
3. Look for: "✅ AWS credentials configured"
4. If successful, proceed to "Validate Prerequisites" stage

## 🚀 **Quick Test Commands**

### **Test AWS Credentials Locally:**
```bash
# Set your credentials
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-west-2

# Test credentials
aws sts get-caller-identity

# Test EKS access
aws eks list-clusters --region us-west-2

# Test CloudFormation access
aws cloudformation list-stacks --region us-west-2
```

### **Test Jenkins Job Parameters:**
```bash
# Check if parameters are set correctly
echo "CLUSTER_NAME: ${CLUSTER_NAME}"
echo "AWS_REGION: ${AWS_REGION}"
echo "AWS_CREDENTIALS: ${AWS_CREDENTIALS}"
```

## 📋 **Pre-flight Checklist**

Before running the Jenkins job, ensure:

- [ ] AWS credentials are created in Jenkins
- [ ] AWS credentials have required permissions
- [ ] Selected region supports EKS
- [ ] No existing cluster with the same name
- [ ] Sufficient AWS quotas for EC2 and EKS
- [ ] Jenkins has internet access to AWS APIs

## 🆘 **Still Having Issues?**

1. **Check Jenkins logs** for detailed error messages
2. **Verify AWS credentials** with `aws sts get-caller-identity`
3. **Test region availability** with `aws eks list-clusters`
4. **Check AWS quotas** in the AWS Console
5. **Review IAM permissions** for the AWS user/role

The most common issue is missing or incorrect AWS credentials configuration! 🔐
