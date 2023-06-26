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
           sh "docker run automation-tests pytest -s ${SUITE_NAME} -alluredir='allure-results'"
//            sh "sudo chmod -R 777 allure-results"
         }
     }
     stage('Reports') {
        steps {
           allure([
      	   includeProperties: false,
      	   jdk: '',
      	   properties: [],
      	   reportBuildPolicy: 'ALWAYS',
      	   results: [[path: 'report']]
    	   ])
  	        }
         }
     }
}