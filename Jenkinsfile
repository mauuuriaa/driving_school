pipeline {
    agent any

    environment {
        IMAGE_BACKEND = 'driving-school-backend'
        IMAGE_WEB = 'driving-school-web'
        TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker check') {
            steps {
                bat 'docker version'
                bat 'docker compose version'
            }
        }

        stage('Build images') {
            steps {
                bat 'docker build -t %IMAGE_BACKEND%:test .'
                bat 'docker build -t %IMAGE_WEB%:test .\\client'
            }
        }

        stage('Test') {
            steps {
                bat 'docker run --rm %IMAGE_BACKEND%:test python manage.py test'
            }
        }

        stage('Build release images') {
            when {
                branch 'main'
            }
            steps {
                bat 'docker compose build backend web'
            }
        }

        stage('Publish to Docker Hub') {
            when {
                branch 'main'
            }
            environment {
                DOCKER_CONFIG = "${WORKSPACE}\\.docker"
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
                    bat 'echo %DH_PASS%| docker login -u %DH_USER% --password-stdin'
                    bat 'docker push %DH_USER%/driving-school-backend:%TAG%'
                    bat 'docker push %DH_USER%/driving-school-web:%TAG%'
                }
            }
            post {
                always {
                    bat(returnStatus: true, script: 'docker logout')
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                bat 'docker compose up -d'
                bat '''
                    powershell -NoProfile -Command "Start-Sleep -Seconds 15; (Invoke-WebRequest -UseBasicParsing http://localhost:8088/api/schools/).StatusCode"
                '''
            }
        }
    }
}