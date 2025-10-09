pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Target deployment environment'
        )
        string(
            name: 'BRANCH',
            defaultValue: 'main',
            description: 'Git branch to build'
        )
        choice(
            name: 'DEPLOY_STRATEGY',
            choices: ['rolling', 'blue-green', 'canary'],
            description: 'Deployment strategy'
        )
        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run automated tests'
        )
        choice(
            name: 'NOTIFICATION_CHANNEL',
            choices: ['email', 'slack', 'teams', 'none'],
            description: 'Notification channel'
        )
        string(
            name: 'DOCKER_TAG',
            defaultValue: 'latest',
            description: 'Docker image tag'
        )
        choice(
            name: 'RESOURCE_LIMITS',
            choices: ['small', 'medium', 'large'],
            description: 'Resource allocation'
        )
        booleanParam(
            name: 'BACKUP_ENABLED',
            defaultValue: false,
            description: 'Enable backup before deployment'
        )
    }
    
    stages {
        stage('🎛️ PARAMETERIZED BUILD POWER') {
            steps {
                echo '✅ This is a PARAMETERIZED build - maximum flexibility!'
                echo "🌍 Environment: ${params.ENVIRONMENT}"
                echo "🌿 Branch: ${params.BRANCH}"
                echo "🚀 Deploy Strategy: ${params.DEPLOY_STRATEGY}"
                echo "🧪 Run Tests: ${params.RUN_TESTS}"
                echo "📧 Notification: ${params.NOTIFICATION_CHANNEL}"
                echo "🐳 Docker Tag: ${params.DOCKER_TAG}"
                echo "💾 Resource Limits: ${params.RESOURCE_LIMITS}"
                echo "💾 Backup Enabled: ${params.BACKUP_ENABLED}"
            }
        }
        
        stage('🔍 Dynamic Code Quality Check') {
            steps {
                echo "Running code quality checks for ${params.ENVIRONMENT} environment..."
                script {
                    if (params.ENVIRONMENT == 'production') {
                        echo '🔒 Running enhanced security checks for production'
                        sh 'echo "Security scan completed"'
                    } else {
                        echo '🔍 Running standard quality checks'
                        sh 'echo "Quality check completed"'
                    }
                }
            }
        }
        
        stage('🧪 Conditional Testing') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                echo "Running tests for ${params.ENVIRONMENT} environment..."
                script {
                    switch(params.ENVIRONMENT) {
                        case 'dev':
                            echo '🧪 Running unit tests only'
                            sh 'echo "Unit tests completed"'
                            break
                        case 'staging':
                            echo '🧪 Running unit + integration tests'
                            sh 'echo "Unit and integration tests completed"'
                            break
                        case 'production':
                            echo '🧪 Running full test suite + smoke tests'
                            sh 'echo "Full test suite completed"'
                            break
                    }
                }
            }
        }
        
        stage('🐳 Dynamic Container Build') {
            steps {
                echo "Building Docker image with tag: ${params.DOCKER_TAG}"
                script {
                    def imageTag = "${params.ENVIRONMENT}-${params.DOCKER_TAG}"
                    echo "🐳 Building image: ${imageTag}"
                    sh "echo 'Image built: ${imageTag}'"
                }
            }
        }
        
        stage('💾 Conditional Backup') {
            when {
                expression { params.BACKUP_ENABLED == true }
            }
            steps {
                echo "Creating backup before ${params.ENVIRONMENT} deployment..."
                sh 'echo "Backup completed successfully"'
            }
        }
        
        stage('🚀 Dynamic Deployment') {
            steps {
                echo "Deploying to ${params.ENVIRONMENT} using ${params.DEPLOY_STRATEGY} strategy..."
                script {
                    switch(params.DEPLOY_STRATEGY) {
                        case 'rolling':
                            echo '🔄 Performing rolling deployment'
                            sh 'echo "Rolling deployment completed"'
                            break
                        case 'blue-green':
                            echo '🔵🟢 Performing blue-green deployment'
                            sh 'echo "Blue-green deployment completed"'
                            break
                        case 'canary':
                            echo '🐦 Performing canary deployment'
                            sh 'echo "Canary deployment completed"'
                            break
                    }
                }
            }
        }
        
        stage('📊 Resource Configuration') {
            steps {
                echo "Configuring resources for ${params.RESOURCE_LIMITS} allocation..."
                script {
                    switch(params.RESOURCE_LIMITS) {
                        case 'small':
                            echo '💾 Small resources: 1 CPU, 512MB RAM'
                            break
                        case 'medium':
                            echo '💾 Medium resources: 2 CPU, 1GB RAM'
                            break
                        case 'large':
                            echo '💾 Large resources: 4 CPU, 2GB RAM'
                            break
                    }
                }
            }
        }
        
        stage('📧 Dynamic Notification') {
            when {
                expression { params.NOTIFICATION_CHANNEL != 'none' }
            }
            steps {
                echo "Sending notification via ${params.NOTIFICATION_CHANNEL}..."
                script {
                    switch(params.NOTIFICATION_CHANNEL) {
                        case 'email':
                            echo '📧 Sending email notification'
                            sh 'echo "Email notification sent"'
                            break
                        case 'slack':
                            echo '💬 Sending Slack notification'
                            sh 'echo "Slack notification sent"'
                            break
                        case 'teams':
                            echo '📱 Sending Teams notification'
                            sh 'echo "Teams notification sent"'
                            break
                    }
                }
            }
        }
        
        stage('✅ PARAMETERIZED BUILD SUCCESS') {
            steps {
                echo '🎉 PARAMETERIZED BUILD ADVANTAGES:'
                echo '   ✅ Dynamic configuration based on parameters'
                echo '   ✅ Multi-environment support in one job'
                echo '   ✅ User-controlled customization'
                echo '   ✅ Conditional logic and workflows'
                echo '   ✅ Flexible deployment strategies'
                echo '   ✅ Smart resource allocation'
                echo '   ✅ Multiple notification channels'
                echo '   ✅ Single job handles all scenarios'
                echo '   ✅ Easy maintenance and updates'
                echo '   ✅ Maximum flexibility and control'
                echo ''
                echo '🚀 This is the power of parameterized builds!'
            }
        }
    }
    
    post {
        always {
            echo "Parameterized build completed for ${params.ENVIRONMENT} environment!"
        }
        success {
            echo '✅ Build succeeded with all parameters applied'
        }
        failure {
            echo '❌ Build failed - check parameters and configuration'
        }
    }
}
