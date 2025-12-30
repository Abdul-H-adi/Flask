pipeline {
    agent any

    triggers {
        // Works when GitHub webhook is configured
        githubPush()
    }

    environment {
        VENV = ".venv"
        DEPLOY_DIR = "/tmp/flask_deploy_target"
        APP_ZIP = "flask_app_build.zip"
    }

    stages {

        stage('Clone Repository') {
            steps {
                // Jenkins will checkout the repo configured in the job
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv "${VENV}"
                    . "${VENV}/bin/activate"
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . "${VENV}/bin/activate"
                    pytest -q
                '''
            }
        }

        stage('Build App') {
            steps {
                sh '''
                    rm -f "${APP_ZIP}"
                    zip -r "${APP_ZIP}" app.py requirements.txt tests README.md
                '''
            }
        }

        stage('Deploy App (Simulated)') {
            steps {
                sh '''
                    sudo mkdir -p "${DEPLOY_DIR}" || mkdir -p "${DEPLOY_DIR}"
                    sudo rm -rf "${DEPLOY_DIR}/app" 2>/dev/null || true
                    sudo mkdir -p "${DEPLOY_DIR}/app" || true

                    # Copy build artifact + app files (simulate deployment)
                    sudo cp -f "${APP_ZIP}" "${DEPLOY_DIR}/" 2>/dev/null || cp -f "${APP_ZIP}" "${DEPLOY_DIR}/"
                    sudo cp -f app.py requirements.txt "${DEPLOY_DIR}/app/" 2>/dev/null || cp -f app.py requirements.txt "${DEPLOY_DIR}/app/"

                    echo "Deployed to: ${DEPLOY_DIR}"
                    ls -la "${DEPLOY_DIR}" || true
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "${APP_ZIP}", fingerprint: true
        }
    }
}
