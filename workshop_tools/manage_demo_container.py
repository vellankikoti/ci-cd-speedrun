pipeline {
    agent any

    parameters {
        string(
            name: 'APP_VERSION',
            defaultValue: '1',
            description: 'Which app version (1-5) do you want to build and run?'
        )
    }

    environment {
        CONTAINER_NAME = "chaos-app-v${params.APP_VERSION}"
        IMAGE_TAG = "ci-cd-chaos-app:v${params.APP_VERSION}"
        DOCKERFILE_PATH = "Jenkins/jenkins_scenarios/scenario_01_docker_build/Dockerfile"
    }

    stages {

        stage('Pre-Cleanup') {
            steps {
                sh '''
                    echo "🔪 Pre-cleanup: Killing any leftover app containers..."

                    # Remove any container using port 3000
                    docker ps -q --filter publish=3000 | xargs -r docker rm -f || true

                    # Remove old container by name
                    docker ps -a --filter "name=$CONTAINER_NAME" -q | xargs -r docker rm -f || true
                '''
            }
        }

        stage('Clone Repo Manually') {
            steps {
                sh '''
                    rm -rf repo
                    git clone --single-branch --branch phase-3-jenkins https://github.com/vellankikoti/ci-cd-chaos-workshop.git repo
                '''
            }
        }

        stage('Verify Workspace') {
            steps {
                sh '''
                    cd repo
                    echo "=== WORKSPACE ==="
                    pwd
                    echo "=== Repo contents ==="
                    ls -la
                    echo "=== Checking Dockerfile path ==="
                    ls -la Jenkins/jenkins_scenarios/scenario_01_docker_build

                    if [ ! -f Jenkins/jenkins_scenarios/scenario_01_docker_build/Dockerfile ]; then
                        echo "ERROR: Dockerfile missing!"
                        exit 1
                    else
                        echo "✅ Dockerfile found!"
                    fi
                '''
            }
        }

        stage('Validate Version') {
            steps {
                script {
                    def allowedVersions = ['1','2','3','4','5']
                    if (!allowedVersions.contains(params.APP_VERSION)) {
                        echo '''
🚫 CHAOS AGENT STRIKES AGAIN! 🚫
Invalid version!

Valid versions are: 1, 2, 3, 4, 5.
'''
                        error("Invalid APP_VERSION: ${params.APP_VERSION}")
                    } else {
                        echo "✅ Version ${params.APP_VERSION} selected. Proceeding..."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    cd repo
                    docker build -t $IMAGE_TAG \\
                        --build-arg APP_VERSION=${params.APP_VERSION} \\
                        -f $DOCKERFILE_PATH \\
                        .
                """
            }
        }

        stage('Run App Container') {
            steps {
                sh """
                    docker run -d --name $CONTAINER_NAME \\
                        -p 3000:3000 \\
                        $IMAGE_TAG
                """
            }
        }

        stage('Check App Logs') {
            steps {
                sh """
                    sleep 5
                    echo "=== Container Logs ==="
                    docker logs $CONTAINER_NAME
                """
            }
        }

        stage('Test App HTTP Response') {
            steps {
                sh '''
                    sleep 3
                    docker exec $CONTAINER_NAME sh -c "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000" > status.txt
                    STATUS_CODE=$(cat status.txt)
                    echo "HTTP Status: $STATUS_CODE"
                    if [ "$STATUS_CODE" -ne 200 ]; then
                        echo "❌ App did not respond correctly!"
                        exit 1
                    else
                        echo "✅ App responded successfully!"
                    fi
                '''
            }
        }

        // No Final Cleanup stage anymore!
    }

    post {
        always {
            echo "✨ Chaos Agent defeated… for now! Pipeline finished."
        }
    }
}
