pipeline {
    agent any

     environment {
        DJANGO_SETTINGS_MODULE = 'todo_list.settings.settings'
        PYTHONPATH = "/usr/src/app"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t todo-app-web:latest .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker-compose run web pytest'
            }
        }
        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['my-ec2-key']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@54.209.119.85 << EOF
                    docker-compose down
                    docker pull tododeploytest/todo-app-web:latest
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
