pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'todo_list.settings'
        PYTHONPATH = "/usr/src/app"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t todoawsimg:latest .'
                sh 'docker tag todoawsimg:latest myusername/todoawsimg:latest'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'dockerid', variable: 'DOCKERHUB_PASSWORD')]) {
                        sh 'echo $DOCKERHUB_PASSWORD | docker login -u nibin42 --password-stdin'
                        sh 'docker push nibin42/todoawsimg:latest'
                    }
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image("nibin42/todoawsimg").inside {
                        sh 'pytest --ds=todo_list.settings'
                    }
                }
            }
        }
        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['my-ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@54.209.119.85 << EOF
                    docker-compose down
                    docker pull nibin42/todoawsimg:latest
                    docker-compose up -d
                    EOF
                    '''
                }
            }
        }
        stage('Switch Green/Blue') {
            steps {
                sshagent (credentials: ['my-ec2-key']) {
                    sh '''
                    ssh ubuntu@54.209.119.85 "sed -i 's/web_green/web_blue/' /path/to/nginx.conf && sudo systemctl restart nginx"
                    '''
                }
            }
        }
    }
}
