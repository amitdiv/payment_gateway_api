mport groovy.json.JsonSlurper
import groovy.json.JsonParserType

String branchName = "dev"
def gitCredentials = null
String repoUrl = "https://github.com/amitdiv/payment_gateway_api.git"
def script_path = "C:\\dummy_environmeent\\"
def retval = []
def count=0
def readfile = 'C:\\dummy_environmeent\\db_data.csv'
def status = 0

node {
  // Start Stages
  stage('Clone') {
      // Clones the repository from the current branch name
      echo 'Make the output directory'
      //bat 'set FLASK_ENV=development;set FLASK_APP=processPayment.py;flask run'
      ////cd C:\\dummy_environmeent
      retval = bat(
          returnStdout: true,
          script: """
          python  """+script_path+"""mysqldb_connect.py
        """
    ).trim()
    echo 'Cloning files from (branch: "' + branchName + '" )'
  }
  stage('Execute') {
      try {
          //println(retval.getClass())
          //println(retval)
          def data = readFile(readfile).split('\n')
          for (d in data) {
              def l = d.split(',').collect{it as String}
              println(l)
       } except (Exception e) {
          status = 1
       }
      }
      def listener = { result -> println "Execution completed with result :: $result" }
      if (status == 0 ) {
          listener.call("pass")
      } else {
          listener.call("fail")
      }
  }
}
