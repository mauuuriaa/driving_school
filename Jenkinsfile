pipeline {
    agent any

    environment {
        VENV = 'venv'
        PYTHON = 'C:\\Users\\Maria\\miniconda3\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup venv') {
            steps {
                bat '"%PYTHON%" -m venv %VENV%'
                bat '%VENV%\\Scripts\\python --version'
                bat '%VENV%\\Scripts\\python -m pip install --upgrade pip'
            }
        }
        stage('Install libs') {
            steps {
                bat '%VENV%\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat '%VENV%\\Scripts\\python manage.py test'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                bat(returnStatus: true, script: '''
                    for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8001" ^| findstr "LISTENING"') do taskkill /F /PID %%a
                    for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5174" ^| findstr "LISTENING"') do taskkill /F /PID %%a
                ''')

                // Создать/обновить таблицы базы данных
                bat '%VENV%\\Scripts\\python manage.py migrate --noinput'

                // Установить зависимости клиента
                dir('client') {
                    bat 'npm install'
                }

                // Запустить сервер и клиент в фоне
                withEnv(['JENKINS_NODE_COOKIE=dontKillMe', 'BUILD_ID=dontKillMe', 'API_TARGET=http://127.0.0.1:8001']) {
                    bat '''
                        powershell -NoProfile -Command "Start-Process -FilePath '%CD%\\%VENV%\\Scripts\\python.exe' -ArgumentList 'manage.py','runserver','127.0.0.1:8001','--noreload' -WorkingDirectory '%CD%' -RedirectStandardOutput '%CD%\\server.log' -RedirectStandardError '%CD%\\server-error.log' -WindowStyle Hidden"
                        powershell -NoProfile -Command "Start-Process -FilePath 'npm.cmd' -ArgumentList 'run','dev','--','--host','127.0.0.1','--port','5174','--strictPort' -WorkingDirectory '%CD%\\client' -RedirectStandardOutput '%CD%\\client.log' -RedirectStandardError '%CD%\\client-error.log' -WindowStyle Hidden"
                    '''
                }

                //  Проверить, что отвечают и сервер, и клиент (через прокси)
                bat '''
                    powershell -NoProfile -Command "Start-Sleep -Seconds 20; (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8001/api/schools/).StatusCode; (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:5174/api/schools/).StatusCode"
                '''
            }
        }
    }
}