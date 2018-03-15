pipeline {
  agent {
    node {
      label 'master'
    }
    
  }
  stages {
    stage('Update Offline') {
      steps {
        echo 'Creating Offline Repo'
        bat 'update-offline-conda-repo.cmd'
        cleanWs()
      }
    }
  }
  environment {
    OFFLINE_CONDA_REPO = 'X:\\pytho-offline-repo'
    CONDAROOT = 'C:\\Users\\brandolinid\\AppData\\Local\\Continuum\\miniconda2'
  }
}