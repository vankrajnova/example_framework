pipeline {
  agent any
  stages {
//      stage("Build image") {
//         steps {
//     	catchError {
//       	   script {
//         	      docker.build("automation-tests", "-f Dockerfile .")
//       	     }
//           }
//        }
//     }
     stage('Run tests') {
        steps {
           sh "docker-compose up -d --build"
           sh "sudo chmod -R 777 allure-results"
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