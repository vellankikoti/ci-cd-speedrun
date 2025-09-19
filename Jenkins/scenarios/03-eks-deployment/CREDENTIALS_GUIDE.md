# AWS Credentials and Region Configuration Guide

## 🔐 **Where Credentials and Region Details Are Passed**

### **1. Jenkins Pipeline Parameters**

The Jenkins pipeline accepts credentials and region through these parameters:

```groovy
parameters {
    // Region parameter
    string(
        name: 'AWS_REGION',
        defaultValue: 'us-west-2',
        description: 'AWS region for EKS cluster deployment'
    )
    
    // AWS Credentials parameter
    credentials(
        name: 'AWS_CREDENTIALS',
        credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        defaultValue: '',
        description: 'AWS Access Key ID and Secret Access Key (Username=Access Key, Password=Secret Key)'
    )
}
```

### **2. Environment Variables**

The pipeline sets up environment variables from parameters:

```groovy
environment {
    AWS_REGION = "${params.AWS_REGION}"
    AWS_DEFAULT_REGION = "${params.AWS_REGION}"
    CLUSTER_NAME = "${params.CLUSTER_NAME}-${BUILD_NUMBER}"
    STACK_NAME = "${params.CLUSTER_NAME}-${BUILD_NUMBER}"
}
```

### **3. Credential Injection in Each Stage**

Every stage that needs AWS access uses `withCredentials` to inject credentials:

```groovy
withCredentials([usernamePassword(
    credentialsId: "${params.AWS_CREDENTIALS}", 
    usernameVariable: 'AWS_ACCESS_KEY_ID', 
    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
)]) {
    sh '''
        # Set AWS credentials
        export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
        export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
        export AWS_DEFAULT_REGION=${AWS_REGION}
        
        # Configure AWS CLI
        aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
        aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
        aws configure set default.region ${AWS_REGION}
        
        # Your AWS commands here...
    '''
}
```

## 🚀 **How to Set Up Credentials in Jenkins**

### **Step 1: Create AWS Credentials in Jenkins**

1. **Go to Jenkins Dashboard**
2. **Click "Manage Jenkins"**
3. **Click "Manage Credentials"**
4. **Click on your domain (usually "Global")**
5. **Click "Add Credentials"**
6. **Select "Username with password"**
7. **Fill in the details**:
   - **Username**: Your AWS Access Key ID
   - **Password**: Your AWS Secret Access Key
   - **ID**: `aws-workshop-credentials` (or any name you prefer)
   - **Description**: "AWS credentials for EKS workshop"
8. **Click "OK"**

### **Step 2: Configure the Jenkins Job**

1. **Go to your EKS job**
2. **Click "Configure"**
3. **In the "Build with Parameters" section**:
   - **AWS_REGION**: Select your preferred region (e.g., `us-west-2`)
   - **AWS_CREDENTIALS**: Select the credentials you created in Step 1
   - **CLUSTER_NAME**: Enter your cluster name (e.g., `my-workshop-cluster`)
   - **NODE_INSTANCE_TYPE**: Select `t3.small` for cost optimization
   - **NODE_COUNT**: Enter `3` (or your preferred number)
   - **ENABLE_LOGGING**: Check `true`
   - **ENABLE_ALB_CONTROLLER**: Check `true`
4. **Click "Save"**

## 🔧 **Alternative: Using AWS IAM Roles (Recommended for Production)**

### **For Jenkins on EC2 with IAM Role**

If Jenkins is running on an EC2 instance, you can use IAM roles instead of credentials:

```groovy
// Remove the credentials parameter and withCredentials blocks
// The EC2 instance will automatically use its IAM role

environment {
    AWS_REGION = "${params.AWS_REGION}"
    AWS_DEFAULT_REGION = "${params.AWS_REGION}"
    // No need to set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
}
```

### **Required IAM Permissions**

The AWS credentials or IAM role needs these permissions:

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

## 📋 **Step-by-Step Setup Process**

### **1. Prepare AWS Credentials**

```bash
# Get your AWS credentials
aws configure list

# Or create new access keys in AWS Console:
# IAM → Users → Your User → Security Credentials → Create Access Key
```

### **2. Create Jenkins Credentials**

1. **Jenkins Dashboard** → **Manage Jenkins** → **Manage Credentials**
2. **Add Credentials** → **Username with password**
3. **Username**: `AKIA...` (your AWS Access Key ID)
4. **Password**: `...` (your AWS Secret Access Key)
5. **ID**: `aws-workshop-credentials`
6. **Description**: `AWS credentials for EKS workshop`

### **3. Create Jenkins Job**

1. **New Item** → **Pipeline**
2. **Job name**: `EKS-Workshop-Deployment`
3. **Pipeline** → **Pipeline script from SCM**
4. **SCM**: `Git`
5. **Repository URL**: `https://github.com/vellankikoti/ci-cd-chaos-workshop.git`
6. **Script Path**: `Jenkins/scenarios/03-eks-deployment/Jenkinsfile`

### **4. Run the Job**

1. **Click "Build with Parameters"**
2. **Select your credentials** from the dropdown
3. **Set region** (e.g., `us-west-2`)
4. **Set cluster name** (e.g., `my-workshop-cluster`)
5. **Click "Build"**

## 🔍 **How Credentials Flow Through the Pipeline**

```
Jenkins Parameters
       ↓
Environment Variables
       ↓
withCredentials Block
       ↓
Shell Environment
       ↓
AWS CLI Configuration
       ↓
Python Scripts (eks_manager.py)
       ↓
AWS SDK (boto3)
       ↓
AWS Services (EKS, EC2, IAM, CloudFormation)
```

## 🛠️ **Troubleshooting Credentials**

### **Common Issues:**

1. **"No credentials found"**
   - Check that credentials are created in Jenkins
   - Verify the credential ID matches the parameter

2. **"Access denied"**
   - Check AWS permissions
   - Verify the access key is active
   - Ensure the region supports EKS

3. **"Invalid credentials"**
   - Verify the access key and secret key are correct
   - Check if the access key is deactivated

### **Debug Commands:**

```bash
# Check AWS credentials
aws sts get-caller-identity

# Check AWS region
aws configure get region

# List available regions
aws ec2 describe-regions --query 'Regions[].RegionName'
```

## 📊 **Security Best Practices**

1. **Use IAM Roles** instead of access keys when possible
2. **Rotate credentials** regularly
3. **Use least privilege** - only grant necessary permissions
4. **Monitor usage** with AWS CloudTrail
5. **Use different credentials** for different environments

## 🎯 **Quick Test**

To verify your setup works:

```bash
# Test AWS credentials
aws sts get-caller-identity

# Test region
aws eks list-clusters --region us-west-2

# Test EKS permissions
aws eks describe-cluster --name test-cluster --region us-west-2
```

The credentials and region are now properly configured throughout the entire pipeline! 🎉
