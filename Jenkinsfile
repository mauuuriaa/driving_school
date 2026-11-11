pipeline {
    agent any

    environment {
        IMAGE_ACCOUNTS = 'driving-school-accounts'
        IMAGE_SCHOOL = 'driving-school-school'
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
                bat 'docker build -t %IMAGE_ACCOUNTS%:test services/accounts'
                bat 'docker build -t %IMAGE_SCHOOL%:test services/school'
                bat 'docker build -t %IMAGE_WEB%:test client'
            }
        }

        stage('Test') {
            steps {
                bat 'docker run --rm %IMAGE_ACCOUNTS%:test python manage.py test'
                bat 'docker run --rm %IMAGE_SCHOOL%:test python manage.py test'
            }
        }

        stage('Build release images') {
            when {
                branch 'main'
            }
            steps {
                bat 'docker compose build accounts school web'
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
                    bat 'docker push %DH_USER%/driving-school-accounts:%TAG%'
                    bat 'docker push %DH_USER%/driving-school-school:%TAG%'
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
                    powershell -NoProfile -Command "Start-Sleep -Seconds 25; (Invoke-WebRequest -UseBasicParsing http://localhost:8088/api/schools/).StatusCode; (Invoke-WebRequest -UseBasicParsing http://localhost:8088/api/users/my/).StatusCode"
                '''
            }
        }
    }
}