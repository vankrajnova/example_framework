pipeline {
  agent any
  stages {
     stage("Build image") {
        steps {
    	catchError {
      	   script {
        	      docker.build("automation-tests", "-f Dockerfile .")
      	     }
          }
       }
    }
     stage('Run tests') {
        steps {
           sh "docker run --name docker_autotests automation-tests pytest -v ${SUITE_NAME}"
           sh "docker cp docker_autotests:${WORKSPACE}/allure_results ."
         }
     }
     stage('Reports') {
        steps {
           allure([
      	   includeProperties: false,
      	   jdk: '',
      	   properties: [],
      	   reportBuildPolicy: 'ALWAYS',
      	   results: [[path: 'allure-results']]
    	   ])
  	        }
         }
     }
}