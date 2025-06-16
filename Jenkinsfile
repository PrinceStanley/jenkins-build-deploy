pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: docker
      image: docker:24.0.7-dind
      securityContext:
        privileged: true
      volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
    - name: kubectl
      image: bitnami/kubectl:1.29
      command:
        - cat
      tty: true
    - name: aws
      image: amazon/aws-cli:2.15.40
      command:
        - cat
      tty: true
  volumes:
    - name: docker-sock
      emptyDir: {}
"""
        }
    }

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = 'your-account-id.dkr.ecr.us-east-1.amazonaws.com/your-ecr-repo'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        KUBE_CONFIG = credentials('kubeconfig-credentials-id')
        AWS_CREDENTIALS = credentials('aws-credentials-id')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    script {
                        dockerImage = docker.build("${ECR_REPO}:${IMAGE_TAG}")
                    }
                }
            }
        }

        stage('Login to ECR') {
            steps {
                container('aws') {
                    script {
                        sh """
                            aws ecr get-login-password --region $AWS_REGION | \
                            docker login --username AWS --password-stdin $ECR_REPO
                        """
                    }
                }
            }
        }

        stage('Push to ECR') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry("https://${ECR_REPO}", '') {
                            dockerImage.push()
                        }
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-credentials-id', variable: 'KUBECONFIG')]) {
                        sh """
                            sed -i 's|image:.*|image: ${ECR_REPO}:${IMAGE_TAG}|' app-deploy.yaml
                            kubectl apply -f app-deploy.yaml
                            kubectl apply -f app-service.yaml
                            kubectl apply -f app-ingress.yaml
                            kubectl rollout status deployment/your-deployment --namespace=your-namespace
                        """
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                currentBuild.result = 'FAILURE'
                echo "Build failed. Please check the logs for more details."
            }
        }
        success {
            script {
                currentBuild.result = 'SUCCESS'
                echo "Build and deployment succeeded."
            }
        }
        always {
            cleanWs()
        }
    }
}
