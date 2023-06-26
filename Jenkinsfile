pipeline {
  agent any
  stages {
     stage("Build image") {
        steps {
    	    sh "docker build -t automation-tests ."
       }
    }
     stage('Run tests') {
        steps {
            sh "docker run automation-tests"
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