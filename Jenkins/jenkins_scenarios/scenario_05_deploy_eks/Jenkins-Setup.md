# 🔐 Jenkins AWS Authentication Setup Instructions

## Step 1: Jenkins Plugins Required

Ensure these plugins are installed in Jenkins:

```bash
# Core required plugins (usually pre-installed):
- Pipeline: Declarative
- Docker Pipeline
- Credentials Plugin
- Credentials Binding Plugin

# Optional but recommended:
- Blue Ocean (for better pipeline visualization)
- HTML Publisher (for report viewing)
```

**Installation via Jenkins UI:**
1. Manage Jenkins → Manage Plugins → Available
2. Search for and install the plugins above
3. Restart Jenkins when prompted

## Step 2: Create AWS Credentials in Jenkins

### Method A: AWS Access Keys (Recommended for simplicity)

1. **In Jenkins UI, navigate to:**
   ```
   Manage Jenkins → Manage Credentials → System → Global credentials (unrestricted)
   ```

2. **Click "Add Credentials"**

3. **Configure the credential:**
   ```
   Kind: Username with password
   Scope: Global
   Username: YOUR_AWS_ACCESS_KEY_ID
   Password: YOUR_AWS_SECRET_ACCESS_KEY
   ID: aws-credentials
   Description: AWS credentials for EKS access
   ```

### Method B: Alternative - Secret Text (if you prefer separate secrets)

Create two separate credentials:

**AWS Access Key ID:**
```
Kind: Secret text
Scope: Global
Secret: YOUR_AWS_ACCESS_KEY_ID
ID: aws-access-key-id
Description: AWS Access Key ID
```

**AWS Secret Access Key:**
```
Kind: Secret text
Scope: Global
Secret: YOUR_AWS_SECRET_ACCESS_KEY
ID: aws-secret-access-key
Description: AWS Secret Access Key
```

## Step 3: Verify AWS Credentials Have Required Permissions

Your AWS credentials need these IAM permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "eks:DescribeCluster",
                "eks:ListClusters",
                "eks:AccessKubernetesApi"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeRegions"
            ],
            "Resource": "*"
        }
    ]
}
```

## Step 4: Create the Jenkins Pipeline Job

1. **Create New Job:**
   ```
   Jenkins Dashboard → New Item → Pipeline
   Name: chaos-workshop-scenario-5-auth-test
   ```

2. **Configure Pipeline:**
   - General → Check "This project is parameterized"
   - Pipeline → Definition: "Pipeline script"
   - Pipeline → Script: [Paste the provided Jenkinsfile]

3. **Save the configuration**

## Step 5: Test the Authentication Pipeline

1. **Build with Parameters:**
   - Click "Build with Parameters"
   - Set your actual cluster name and region
   - Leave RUN_SCENARIO_5 = true
   - Click "Build"

2. **Monitor Console Output:**
   ```
   Expected successful output:
   ✅ AWS authentication successful
   ✅ EKS cluster 'your-cluster' found in region 'your-region'
   ✅ Kubeconfig updated successfully
   ✅ kubectl connectivity confirmed
   ✅ Can create deployments
   ✅ Can create services
   ✅ Can create configmaps
   ```

## Step 6: Alternative Authentication Methods

### Option A: Using AWS IAM Roles (for EC2-hosted Jenkins)

If Jenkins runs on EC2, you can use IAM roles instead:

```groovy
// In Jenkinsfile, replace the withCredentials block with:
sh '''
    echo "🔐 Using EC2 instance role for authentication..."
    
    # Verify instance has AWS credentials
    aws sts get-caller-identity
    
    if [ $? -ne 0 ]; then
        echo "❌ No AWS credentials available via instance role"
        exit 1
    fi
'''
```

### Option B: Using AWS CLI Profiles

If you have AWS CLI profiles configured:

```groovy
environment {
    AWS_PROFILE = "your-profile-name"
    AWS_DEFAULT_REGION = "${params.AWS_REGION}"
}
```

### Option C: Cross-Account Role Assumption

For cross-account access:

```groovy
withCredentials([
    usernamePassword(
        credentialsId: 'aws-credentials', 
        usernameVariable: 'AWS_ACCESS_KEY_ID', 
        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
    )
]) {
    sh '''
        # Assume cross-account role
        ASSUME_ROLE_OUTPUT=$(aws sts assume-role \\
            --role-arn "arn:aws:iam::ACCOUNT-ID:role/ROLE-NAME" \\
            --role-session-name "jenkins-scenario-5-${BUILD_NUMBER}")
        
        # Extract temporary credentials
        export AWS_ACCESS_KEY_ID=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.Credentials.AccessKeyId')
        export AWS_SECRET_ACCESS_KEY=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.Credentials.SecretAccessKey')
        export AWS_SESSION_TOKEN=$(echo $ASSUME_ROLE_OUTPUT | jq -r '.Credentials.SessionToken')
        
        # Continue with EKS operations...
    '''
}
```

## Step 7: Troubleshooting Common Issues

### Issue: "Credentials not found"
```bash
# Solution: Verify credential ID matches exactly
# In Jenkins: Manage Credentials → Check the ID field
# In Pipeline: Ensure credentialsId matches exactly
```

### Issue: "EKS cluster not found"
```bash
# Solution: Check cluster name and region
aws eks list-clusters --region us-west-2
```

### Issue: "kubectl authentication failed"
```bash
# Solution: Check AWS-auth ConfigMap in your cluster
kubectl get configmap aws-auth -n kube-system -o yaml
```

### Issue: "Permission denied" for Kubernetes operations
```bash
# Solution: Update aws-auth ConfigMap to include your user/role
kubectl edit configmap aws-auth -n kube-system

# Add your user ARN to mapUsers section:
mapUsers: |
  - userarn: arn:aws:iam::ACCOUNT-ID:user/USERNAME
    username: USERNAME
    groups:
    - system:masters
```

## Step 8: Security Best Practices

### Credential Security
- ✅ Use Jenkins credentials store (never hardcode)
- ✅ Limit credential scope to specific jobs if possible
- ✅ Rotate AWS keys regularly
- ✅ Use IAM roles when possible instead of access keys

### Network Security
- ✅ Ensure Jenkins can reach EKS API endpoints
- ✅ Configure security groups appropriately
- ✅ Use VPC endpoints for AWS API calls if needed

### Audit and Monitoring
- ✅ Enable AWS CloudTrail for API audit logs
- ✅ Monitor Jenkins build logs for authentication failures
- ✅ Set up alerts for repeated authentication failures

## Step 9: Validation Checklist

Before proceeding to the next step, verify:

- [ ] Jenkins pipeline runs without errors
- [ ] AWS authentication succeeds
- [ ] EKS cluster is accessible
- [ ] kubectl commands work
- [ ] Required Kubernetes permissions are confirmed
- [ ] Environment summary is generated and archived
- [ ] Kubeconfig is saved as Jenkins artifact

## Step 10: Next Steps Preparation

Once authentication works, you'll be ready for:

1. **Docker Image Building**: Building the Scenario 5 container
2. **EKS Deployment**: Running actual deployment tests
3. **Report Generation**: Creating HTML/JSON reports
4. **Artifact Archiving**: Saving results in Jenkins

The authentication pipeline provides the foundation for all subsequent steps by:
- ✅ Establishing AWS connectivity
- ✅ Configuring kubectl access
- ✅ Validating permissions
- ✅ Creating reusable artifacts (kubeconfig, environment summary)

---

## 🎯 **Success Criteria**

Your authentication setup is successful when:
- ✅ Pipeline shows "AWS authentication successful"
- ✅ EKS cluster is found and accessible
- ✅ kubectl can connect to the cluster
- ✅ All required Kubernetes permissions are confirmed
- ✅ kubeconfig and environment-summary.json are archived

**Ready for the next step once this authentication pipeline runs successfully!** 🚀