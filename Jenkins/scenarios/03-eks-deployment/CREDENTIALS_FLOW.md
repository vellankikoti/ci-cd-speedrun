# AWS Credentials and Region Flow Diagram

## 🔄 **Complete Credentials Flow**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           JENKINS JOB CONFIGURATION                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Parameters:                                                                    │
│  ├── AWS_REGION: "us-west-2"                                                   │
│  ├── CLUSTER_NAME: "my-workshop-cluster"                                       │
│  ├── NODE_INSTANCE_TYPE: "t3.small"                                            │
│  ├── NODE_COUNT: "3"                                                           │
│  ├── ENABLE_LOGGING: true                                                      │
│  ├── ENABLE_ALB_CONTROLLER: true                                               │
│  └── AWS_CREDENTIALS: "aws-workshop-credentials" (Jenkins Credential ID)       │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           JENKINS ENVIRONMENT VARIABLES                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  environment {                                                                  │
│    AWS_REGION = "${params.AWS_REGION}"                                         │
│    AWS_DEFAULT_REGION = "${params.AWS_REGION}"                                 │
│    CLUSTER_NAME = "${params.CLUSTER_NAME}-${BUILD_NUMBER}"                     │
│    STACK_NAME = "${params.CLUSTER_NAME}-${BUILD_NUMBER}"                       │
│  }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE STAGES WITH CREDENTIALS                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Each stage uses:                                                               │
│  withCredentials([usernamePassword(                                            │
│    credentialsId: "${params.AWS_CREDENTIALS}",                                 │
│    usernameVariable: 'AWS_ACCESS_KEY_ID',                                      │
│    passwordVariable: 'AWS_SECRET_ACCESS_KEY'                                   │
│  )]) {                                                                          │
│    sh '''                                                                       │
│      export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}                             │
│      export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}                     │
│      export AWS_DEFAULT_REGION=${AWS_REGION}                                   │
│      # AWS commands here...                                                    │
│    '''                                                                          │
│  }                                                                              │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SHELL ENVIRONMENT                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Environment Variables:                                                        │
│  ├── AWS_ACCESS_KEY_ID=AKIA...                                                 │
│  ├── AWS_SECRET_ACCESS_KEY=...                                                 │
│  ├── AWS_DEFAULT_REGION=us-west-2                                              │
│  └── AWS_REGION=us-west-2                                                      │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            AWS CLI CONFIGURATION                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│  aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}                      │
│  aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}              │
│  aws configure set default.region ${AWS_REGION}                                │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PYTHON SCRIPTS                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  eks_manager.py:                                                               │
│  ├── boto3.client('eks', region_name=region)                                   │
│  ├── boto3.client('cloudformation', region_name=region)                        │
│  ├── boto3.client('iam', region_name=region)                                   │
│  └── boto3.client('ec2', region_name=region)                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        ↓
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AWS SERVICES                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  AWS API Calls:                                                                │
│  ├── EKS: Create cluster, describe cluster, update kubeconfig                  │
│  ├── CloudFormation: Create stack, describe stack, get outputs                 │
│  ├── EC2: Create VPC, subnets, security groups, instances                      │
│  ├── IAM: Create roles, policies, OIDC provider                               │
│  └── STS: Get caller identity for validation                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔐 **Credential Storage Locations**

### **1. Jenkins Credential Store**
```
Jenkins → Manage Jenkins → Manage Credentials → Global
├── ID: aws-workshop-credentials
├── Type: Username with password
├── Username: AKIA... (AWS Access Key ID)
└── Password: ... (AWS Secret Access Key)
```

### **2. Pipeline Parameters**
```groovy
parameters {
    credentials(
        name: 'AWS_CREDENTIALS',
        credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
        defaultValue: '',
        description: 'AWS Access Key ID and Secret Access Key'
    )
}
```

### **3. Environment Variables (Runtime)**
```bash
# Set in each pipeline stage
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION=${AWS_REGION}
```

### **4. AWS CLI Configuration**
```bash
# Configured in each stage
aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
aws configure set default.region ${AWS_REGION}
```

## 🛡️ **Security Layers**

### **Layer 1: Jenkins Credential Store**
- Encrypted storage of AWS credentials
- Access control through Jenkins permissions
- Credential rotation support

### **Layer 2: Pipeline Parameter Binding**
- Credentials injected only when needed
- Scoped to specific pipeline runs
- No persistent storage in pipeline code

### **Layer 3: Environment Variable Scope**
- Variables only available within `withCredentials` block
- Automatically cleaned up after stage completion
- No logging of sensitive values

### **Layer 4: AWS CLI Configuration**
- Temporary configuration per stage
- Overwrites any existing configuration
- Cleared after stage completion

## 🔍 **Verification Points**

### **1. Credential Validation**
```bash
# Check if credentials are accessible
aws sts get-caller-identity
```

### **2. Region Validation**
```bash
# Check if region is set correctly
aws configure get region
echo $AWS_DEFAULT_REGION
```

### **3. EKS Permissions**
```bash
# Check EKS access
aws eks list-clusters --region us-west-2
```

### **4. CloudFormation Permissions**
```bash
# Check CloudFormation access
aws cloudformation list-stacks --region us-west-2
```

## 🚨 **Troubleshooting Flow**

```
1. Check Jenkins Credentials
   ↓ (if failed)
2. Check Pipeline Parameters
   ↓ (if failed)
3. Check Environment Variables
   ↓ (if failed)
4. Check AWS CLI Configuration
   ↓ (if failed)
5. Check AWS Permissions
   ↓ (if failed)
6. Check AWS Service Availability
```

## 📋 **Quick Setup Checklist**

- [ ] AWS Access Key ID and Secret Access Key created
- [ ] Jenkins credentials configured with ID `aws-workshop-credentials`
- [ ] Pipeline job created with correct parameters
- [ ] AWS region selected (e.g., `us-west-2`)
- [ ] Required AWS permissions granted
- [ ] Jenkins job run with parameters
- [ ] Credentials validation successful
- [ ] EKS cluster deployment successful

This flow ensures secure, traceable credential management throughout the entire pipeline! 🔐
