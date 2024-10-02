pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'todo_list.settings'
        PYTHONPATH = "/usr/src/app"
    }

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t todoawsimg:latest .'  // Build Docker image
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag todoawsimg:latest nibin42/todoawsimg:latest'  // Tag the image
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Using the Docker access token for authentication
                    withCredentials([string(credentialsId: 'dockertoken', variable: 'DOCKER_TOKEN')]) {
                        sh '''
                        echo "$DOCKER_TOKEN" | docker login -u nibin42 --password-stdin
                        docker push nibin42/todoawsimg:latest
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("nibin42/todoawsimg:latest").inside {
                        sh 'pytest --ds=todo_list.settings'  // Run tests with Django settings
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent (credentials: ['my-ec2-key']) {
                    sh '''
                    ssh -v -o StrictHostKeyChecking=no ubuntu@54.209.119.85 << 'EOF'
                    cd /var/lib/jenkins/workspace/mytodopipeline
                    # Stop the running containers
                    docker-compose down || true

                    # Pull the latest image from Docker Hub
                    docker pull nibin42/todoawsimg:latest

                    # Bring up the services with the latest image
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
                    ssh ubuntu@54.209.119.85 "sed -i 's/web_green/web_blue/' /var/lib/jenkins/workspace/mytodopipeline/nginx/nginx.conf && sudo systemctl restart nginx"
                    '''
                }
            }
        }
    }
}
