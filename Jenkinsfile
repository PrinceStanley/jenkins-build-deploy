pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: jnlp # Jenkins JNLP Agent
      image: jenkins/inbound-agent:latest # Or a specific version like '4.13.2-1'
      env:
        # Replace with your Jenkins service URL that agents can reach
        - name: JENKINS_URL
          value: "http://jenkins.jenkins.svc.cluster.local:8080"
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent/workspace
    - name: docker
      image: docker:20.10-dind
      securityContext:
        privileged: true
      command:
        - dockerd-entrypoint.sh
      args:
        - --host=unix:///var/run/docker.sock
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
        - name: workspace-volume
          mountPath: /home/jenkins/agent/workspace
        - name: docker-sock
          mountPath: /var/run
    - name: aws
      image: 828692096705.dkr.ecr.us-east-1.amazonaws.com/jenkins-agent-ecr-k8s:v2
      command:
        - cat
      tty: true
      volumeMounts:
        - name: docker-graph-storage
          mountPath: /var/lib/docker
        - name: workspace-volume
          mountPath: /home/jenkins/agent/workspace
        - name: docker-sock
          mountPath: /var/run
  volumes:
    - name: docker-graph-storage
      emptyDir: {}
    - name: workspace-volume
      emptyDir: {}
    - name: docker-sock
      emptyDir: {}
"""
        }
    }

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '828692096705.dkr.ecr.us-east-1.amazonaws.com/app-deploy/app'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                container('jnlp') {
                    script {
                        echo "Checking out code from SCM..."
                       // git branch: 'main', credentialsId: 'PrinceGithub', url: 'https://github.com/PrinceStanley/jenkins-build-deploy.git'
                        checkout scm
                        echo "Code checked out successfully."
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('aws') {
                    script {
                        def dockerImage = "${ECR_REPO}:${IMAGE_TAG}"
                        echo "Building Docker image: ${dockerImage}"
                        sh "docker build -t ${dockerImage} ."
                        env.DOCKER_IMAGE = dockerImage
                        echo "Docker image built successfully: ${dockerImage}"
                    }
                }
            }
        }

        stage('Login to ECR') {
            steps {
                container('aws') {
                    script {
                        sh """
                            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
                        """
                    }
                }
            }
        }

        stage('Push to ECR') {
            steps {
                container('aws') {
                    script {
 //                       docker.withRegistry("https://${ECR_REPO}", '') {
 //                           dockerImage.push()
                        sh """
                            docker push ${ECR_REPO}:${IMAGE_TAG}
                        """
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                container('aws') {
                    script {
                         sh """
                            sed -i 's|image:.*|image: ${ECR_REPO}:${IMAGE_TAG}|' app-deploy.yaml
                            kubectl create namespace app --dry-run=client -o yaml | kubectl apply -f -
                            kubectl apply -f app-deploy.yaml -n app
                            kubectl apply -f app-svc.yaml -n app
                            kubectl apply -f app-ingress.yaml -n app
                            kubectl rollout status deployment/app-deploy --namespace=app
                            echo "Deployment to EKS completed successfully."
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
    }
}
