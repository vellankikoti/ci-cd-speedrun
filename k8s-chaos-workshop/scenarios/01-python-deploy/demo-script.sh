#!/bin/bash
# demo-script.sh - Instructor runs this live

echo "🎭 CHAOS AGENT ATTACK: Manual deployment chaos!"
echo "Watch how 'simple' kubectl commands can fail..."

# Attempt 1: Missing namespace
echo "📝 Deploying vote app manually..."
kubectl apply -f chaos/broken-vote-app.yaml
echo "❌ Failed! Missing namespace..."

# Attempt 2: Wrong ConfigMap reference  
echo "📝 Fixing namespace, trying again..."
kubectl create namespace vote-app
kubectl apply -f chaos/broken-vote-app.yaml
echo "❌ Failed! Missing ConfigMap..."

# Attempt 3: Wrong service configuration
echo "📝 Creating ConfigMap manually..."
kubectl create configmap vote-config --from-literal=poll_question="Favorite Language?" -n vote-app
kubectl apply -f chaos/broken-vote-app.yaml
echo "❌ Failed! Service misconfiguration..."

echo "😈 Chaos Agent: 'See? Manual deployments are chaos!'"