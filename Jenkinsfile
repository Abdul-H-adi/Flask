pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        VENV = ".venv"
        DEPLOY_DIR = "C:\\tmp\\flask_deploy_target"
        APP_ZIP = "flask_app_build.zip"
    }

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                    python --version
                    python -m venv %VENV%
                    call %VENV%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Unit Tests') {
            steps {
                bat """
                    call %VENV%\\Scripts\\activate
                    pytest -q
                """
            }
        }

        stage('Build App') {
            steps {
                bat """
                    powershell -NoProfile -Command "if (Test-Path '%APP_ZIP%') { Remove-Item '%APP_ZIP%' -Force }"
                    powershell -NoProfile -Command "Compress-Archive -Path app.py,requirements.txt,tests,README.md -DestinationPath '%APP_ZIP%' -Force"
                """
            }
        }

        stage('Deploy App (Simulated)') {
            steps {
                bat """
                    if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"
                    if not exist "%DEPLOY_DIR%\\app" mkdir "%DEPLOY_DIR%\\app"
                    copy /Y "%APP_ZIP%" "%DEPLOY_DIR%\\"
                    copy /Y "app.py" "%DEPLOY_DIR%\\app\\"
                    copy /Y "requirements.txt" "%DEPLOY_DIR%\\app\\"
                    echo Deployed to: %DEPLOY_DIR%
                    dir "%DEPLOY_DIR%"
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "${APP_ZIP}", fingerprint: true
        }
    }
}
