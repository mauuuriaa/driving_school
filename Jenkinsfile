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
                   echo 'Deploying to production environment...'
               }
           }
       }
   }