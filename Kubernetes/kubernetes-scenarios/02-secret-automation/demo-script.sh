#!/bin/bash
# demo-script.sh - Instructor runs this live

echo "🎭 CHAOS AGENT'S SECURITY ATTACK!"
echo "Watch how exposed secrets create disasters..."

# Attempt 1: Plain text passwords in YAML
echo "📝 Deploying todo app with 'secure' passwords..."
cat chaos/insecure-todo-app.yaml | grep -A 5 -B 5 password
echo "😱 EXPOSED! Database password visible in plain text!"

kubectl apply -f chaos/insecure-todo-app.yaml
echo "❌ Security disaster deployed!"

# Attempt 2: Wrong secret configuration
echo "📝 Trying to fix with Kubernetes secrets..."
kubectl apply -f chaos/broken-secrets.yaml
echo "❌ Secret misconfiguration!"

# Show the security problems
echo "💀 CHAOS AGENT'S DAMAGE:"
echo "   - Passwords visible in YAML files"
echo "   - Secrets stored in Git repositories"
echo "   - No rotation = permanent compromise"
echo "   - No audit trail = invisible breaches"

echo "😈 Chaos Agent: 'Your data belongs to me now!'"