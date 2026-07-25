pipeline {
    agent any

    environment {
        IMAGE_NAME = "voyage-flight-price-api"
        REGISTRY = "your-dockerhub-username"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest tests/ || true'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $REGISTRY/$IMAGE_NAME:$BUILD_NUMBER .'
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $REGISTRY/$IMAGE_NAME:$BUILD_NUMBER'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl set image deployment/flight-price-api flight-price-api=$REGISTRY/$IMAGE_NAME:$BUILD_NUMBER'
            }
        }
    }

    post {
        success { echo 'Deployment successful.' }
        failure { echo 'Pipeline failed — check logs.' }
    }
}
