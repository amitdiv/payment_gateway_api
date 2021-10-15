
node {
    environment { 
        Title = 'qwerty'
    }
    stage('Build') {
        if (env.NAME=="XYZ") {
            println("Build started")
            sh 'python ./processPayment.py'
        } else {
            println("Name is differrent hence printing title :: "+{Title})
        }
    }
    stage('Test') {
        println("test started")
    }
    stage('Deploy') {
        println("deploy started")
    }
}
