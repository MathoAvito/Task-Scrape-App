pipeline {
   agent any
   
   environment {
    ECR_URL = '644435390668.dkr.ecr.eu-west-1.amazonaws.com'
    REPO_NAME = 'matan-task-scrape-portfolio'
   }

   stages {
      stage('Build') {
         steps {
            echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
            echo "*-*-*-*-*-*-*-*-*-*-*-*   Build   *-*-*-*-*-*-*-*-*-*-*-*-*-*-"
            echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"

            script {
               withCredentials([file(credentialsId: 'task-scrape-config', variable: 'config')]) { // app's config file added directly to jenkins and copied to workspace
                  sh 'cp $config ./website/database.env || (rm -f ./website/database.env && cp $config ./website/database.env)'
               }
               sh "docker-compose -f docker-compose-test.yaml build"
            }
         }
      }

      stage ('test') {
         steps {
            echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
            echo "*-*-*-*-*-*-*-*-*-*-*-*   Test   *-*-*-*-*-*-*-*-*-*-*-*-*-*-"
            echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"

            sh 'docker network create test-network || true'
            sh "docker network connect test-network ${HOSTNAME}" //  connect Jenkin's container to the test network
            sh "docker-compose -f docker-compose-test.yaml up -d --build"
            sh '''#!/bin/bash
                COUNT=0
                until $(curl --output /dev/null --silent --head --fail http://frontend); do
                  COUNT=$((COUNT + 1))
                  sleep 5
                  if [[ COUNT -eq 10 ]]; then
                     echo "test failed, exit ..."
                     echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-----LOGS----*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
                     echo "\n=======================\nFRONTEND\n======================="
                     docker logs task-scrape-front
                     echo "===========================================================\n"
                     echo "\n=======================\nBACKEND\n======================="
                     docker logs task-scrape-back
                     echo "==========================================================="
                     exit 1
                  fi
                done
                '''
                // make 10 tries to curl, check that the app is running.
                // if it fails, print the logs of the two containers (front&back)

            cleanWs() // Remove working directory as we need to clone and modify infrastructure repo
         }
      }

      stage('Cloning infra repo') {
         when { expression { env.GIT_BRANCH == 'main' } }
         steps {
            sshagent(credentials: ['github_jenkins']) {
               sh 'git clone git@github.com:MathoAvito/Task-Scrape-GitOps-App.git .'
            }
         }
      }


      stage('Calc and replace to new tag') { 
         when { expression { env.GIT_BRANCH == 'main' } }
         steps {
            script {
               NEXT_TAG = sh(script: "yq e .appVersion Chart.yaml | awk '{print \$1 + 0.01}'", returnStdout: true).trim()
               sh "yq e -i .appVersion='${NEXT_TAG}' Chart.yaml"
            }
         }
      }

      stage('Publish to ECR') {
        when { expression { env.GIT_BRANCH == 'main' } }
        steps {
          script {
            sh "aws ecr get-login-password --region eu-west-1 | \
                docker login --username AWS --password-stdin ${ECR_URL}"

            sh "docker tag task-scrape-back:latest ${ECR_URL}/${REPO_NAME}:backend-${NEXT_TAG}"
            sh "docker push ${ECR_URL}/${REPO_NAME}:backend-${NEXT_TAG}"

            sh "docker tag task-scrape-front:latest ${ECR_URL}/${REPO_NAME}:frontend-${NEXT_TAG}"
            sh "docker push ${ECR_URL}/${REPO_NAME}:frontend-${NEXT_TAG}"
           }
        }
      }

      stage('push changes to infra repo') { // Changing the tag of the app's helm chart. Triggering CD 
         when { expression { env.GIT_BRANCH == 'main' } }
         steps {
            script {
               sshagent(credentials: ['github_jenkins']) {
                  sh """#!/bin/bash
                        git config user.email ${env.GIT_COMMITTER_EMAIL}
                        git config user.name ${env.GIT_COMMITTER_NAME}
                        git add Chart.yaml
                        git commit -am"Done by Jenkins, build number ${BUILD_NUMBER}"
                        git push
                     """
               }
            }
         }
      }
   }

   post {
    always {

//   ############## E-Mail ##############
      emailext body: '${DEFAULT_CONTENT}',
         subject: '${DEFAULT_SUBJECT}',
         to: '${DEFAULT_RECIPIENTS}',
         from: '${env.DEFAULT_FROM_EMAIL}'

//   ############## Cleaning ##############
      sh 'docker rm -f task-scrape-front task-scrape-back mysql'
      sh "docker network disconnect test-network ${HOSTNAME}"
      sh 'docker network rm test-network'
      sh 'docker system prune --all -f'
      cleanWs()
    }
  }
}
