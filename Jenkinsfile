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

stage(stage('Install Dependencies') {
  steps {
    bat """
      py -3.11 --version

      rem Create venv using Python 3.11
      py -3.11 -m venv .venv

      rem Ensure pip exists inside venv
      .venv\\Scripts\\python.exe -m ensurepip --upgrade

      rem Upgrade pip + install requirements
      .venv\\Scripts\\python.exe -m pip install --upgrade pip
      .venv\\Scripts\\python.exe -m pip install -r requirements.txt
    """
  }
}


stage('Run Unit Tests') {
  steps {
    bat """
      .venv\\Scripts\\python.exe -m pytest -q
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
