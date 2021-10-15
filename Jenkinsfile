
node {
    environment { 
        Title = 'qwerty'
    }
    stage('Build') {
        if (env.NAME=="XYZ") {
            println("Build started")
        } else {
            println("Name is differrent hence printing title :: "+env.Title)
        }
    }
    stage('Test') {
        println("test started")
    }
    stage('Deploy') {
        println("deploy started")
    }
}
