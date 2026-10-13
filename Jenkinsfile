pipeline {
    agent any

    environment {
        APP_NAME = "student-performance-app"
        APP_PORT = "5000"
        CONTAINER_PORT = "8080"
        IMAGE_TAG = "student-performance:${BUILD_NUMBER}"
        LATEST_TAG = "student-performance:latest"
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                echo '=== Stage 1: Checking out code from GitHub ==='
                checkout scm
            }
        }

        stage('Set Up Environment & Run Tests') {
            steps {
                echo '=== Stage 2: Installing dependencies and running pytest ==='
                sh '''
                    # Create isolated Python virtual environment for test runner
                    python3 -m venv venv_ci
                    . venv_ci/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    # Run automated unit & integration tests
                    pytest -v
                    
                    # Deactivate virtual environment
                    deactivate
                    rm -rf venv_ci
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '=== Stage 3: Building Docker container image ==='
                sh """
                    docker build -t ${IMAGE_TAG} .
                    docker tag ${IMAGE_TAG} ${LATEST_TAG}
                """
            }
        }

        stage('Deploy Application Container') {
            steps {
                echo '=== Stage 4: Deploying container on EC2 ==='
                sh """
                    # Stop and remove existing running container if present
                    if [ \$(docker ps -q -f name=${APP_NAME}) ]; then
                        echo "Stopping running container ${APP_NAME}..."
                        docker stop ${APP_NAME}
                    fi

                    if [ \$(docker ps -aq -f name=${APP_NAME}) ]; then
                        echo "Removing previous container ${APP_NAME}..."
                        docker rm -f ${APP_NAME}
                    fi

                    # Run new container with port mapping
                    echo "Starting new container ${APP_NAME} on port ${APP_PORT}..."
                    docker run -d \\
                        --name ${APP_NAME} \\
                        --restart always \\
                        -p ${APP_PORT}:${CONTAINER_PORT} \\
                        ${LATEST_TAG}
                """
            }
        }

        stage('Health Check') {
            steps {
                echo '=== Stage 5: Verifying container health ==='
                sh """
                    sleep 10
                    # Check if the HTTP endpoint responds
                    STATUS=\$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${APP_PORT}/ || true)
                    echo "Healthcheck HTTP Status: \$STATUS"
                    if [ "\$STATUS" -eq 200 ]; then
                        echo "Deployment successful and healthy!"
                    else
                        echo "Healthcheck failed with status \$STATUS"
                        exit 1
                    fi
                """
            }
        }
    }

    post {
        always {
            echo '=== Clean up unused docker images ==='
            sh 'docker image prune -f || true'
        }
        success {
            echo "SUCCESS: Pipeline completed and application is running on port ${APP_PORT}!"
        }
        failure {
            echo "FAILURE: Build or deployment failed. Please check logs above."
        }
    }
}
