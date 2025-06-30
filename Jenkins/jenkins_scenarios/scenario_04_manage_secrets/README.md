# 🚀 Scenario 4 – Managing Secrets for AWS

## ✅ Why It Matters

AWS credentials often sit at the heart of your deployments.  
If mishandled, they can:

- Leak into logs
- Expose your AWS account to attackers
- Cause massive cloud bills 💸

> **Chaos Event:**  
> “AWS secret key appears in Jenkins console logs!”

---

## ✅ What You’ll Do

✅ Use Jenkins credentials binding for AWS.  
✅ Mask secrets in console output.  
✅ Prove you can safely call AWS CLI commands in a pipeline.

---

## ✅ How to Run

1. Start Jenkins.

2. Go to:
    ```
    Jenkins > Manage Jenkins > Credentials
    ```

3. Add new credentials:
    - Type: AWS Credentials
    - ID: `aws-credentials`

4. Copy this Jenkinsfile into a pipeline job.

5. Run the job.

---

## ✅ Chaos Fixes

- Never echo secrets directly.  
- Always use credentials binding plugins.  
- Rotate credentials periodically.

---

## ✅ Expected Output

✅ Console log should show:
````

🔐 Running AWS CLI to verify identity...
{
"UserId": "...",
"Account": "...",
"Arn": "arn\:aws\:iam::..."
}

```

✅ No secret keys printed.

---

## ✅ Best Practices

- Use IAM roles where possible instead of static keys.  
- Restrict secrets to minimal permissions.  
- Never commit secrets to Git!

---
