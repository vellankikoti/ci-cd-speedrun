#!/bin/bash

echo "🔌 Installing Required Jenkins Plugins"
echo "====================================="

# Wait for Jenkins to be ready
echo "⏳ Waiting for Jenkins to be ready..."
sleep 30

# Get the admin password
PASSWORD=$(docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null)

if [ -z "$PASSWORD" ]; then
    echo "❌ Could not get Jenkins password. Please check if Jenkins is running."
    exit 1
fi

echo "✅ Jenkins password: $PASSWORD"

# Create a temporary script to install plugins
cat > install_plugins.groovy << 'EOF'
import jenkins.model.*
import hudson.model.*
import hudson.util.*
import hudson.PluginWrapper
import hudson.plugins.*

Jenkins jenkins = Jenkins.getInstance()

// Install Docker Pipeline plugin
def pluginManager = jenkins.getPluginManager()
def uc = jenkins.getUpdateCenter()
uc.updateAllSites()

def plugin = uc.getPlugin('docker-workflow')
if (plugin != null) {
    def future = plugin.deploy()
    future.get()
    println "✅ Docker Pipeline plugin installed successfully"
} else {
    println "❌ Docker Pipeline plugin not found in update center"
}

// Restart Jenkins to apply changes
jenkins.doSafeRestart()
EOF

echo "🔌 Installing Docker Pipeline plugin..."
docker exec jenkins java -jar /usr/share/jenkins/jenkins.war -httpPort=8080 -prefix=/jenkins groovy install_plugins.groovy

echo "✅ Plugin installation initiated!"
echo ""
echo "🎯 NEXT STEPS:"
echo "1. Wait for Jenkins to restart (check http://localhost:8080)"
echo "2. Create your pipeline job"
echo "3. Copy the Jenkinsfile and run your chaos scenarios!"
echo ""
echo "🧹 Clean up: rm install_plugins.groovy" 