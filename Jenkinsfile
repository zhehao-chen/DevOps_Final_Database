@Library('jenkins-shared-library') _

pipeline {
    agent any

    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    environment {
        IMAGE_NAME    = "zhehaochen/database"
        GIT_SHORT     = "${env.GIT_COMMIT?.take(7) ?: 'unknown'}"
        IMAGE_TAG     = "build.${env.BUILD_NUMBER}-git.${GIT_SHORT}"
        ENV_TAG       = "${env.BRANCH_NAME == 'main' ? 'prod-latest' : env.BRANCH_NAME == 'develop' ? 'dev-latest' : 'staging-latest'}"
    }

    stages {

        // ── Stage 1: Build ─────────────────────────────────────────────
        stage('Build') {
            steps {
                script { buildStage() }
            }
        }

        // ── Stage 2: Test ──────────────────────────────────────────────
        stage('Test') {
            steps {
                script { testStage() }
            }
        }

        // ── Stage 3: Security Scan ─────────────────────────────────────
        stage('Security Scan') {
            steps {
                script { securityScanStage() }
            }
        }

        // ── Stage 4: Container Build ───────────────────────────────────
        stage('Container Build') {
            when {
                anyOf {
                    branch 'develop'
                    branch pattern: 'release/.*', comparator: 'REGEXP'
                    branch 'main'
                }
            }
            steps {
                script { containerBuildStage(env.IMAGE_NAME, env.IMAGE_TAG, env.ENV_TAG) }
            }
        }

        // ── Stage 5: Container Push ────────────────────────────────────
        stage('Container Push') {
            when {
                anyOf {
                    branch 'develop'
                    branch pattern: 'release/.*', comparator: 'REGEXP'
                    branch 'main'
                }
            }
            steps {
                script { containerPushStage(env.IMAGE_NAME, env.IMAGE_TAG, env.ENV_TAG) }
            }
        }

        // ── Stage 6: Deploy ────────────────────────────────────────────
        stage('Deploy to Dev') {
            when { branch 'develop' }
            steps {
                script { deployStage('dev', env.IMAGE_NAME, env.IMAGE_TAG) }
            }
        }

        stage('Deploy to Staging') {
            when { branch pattern: 'release/.*', comparator: 'REGEXP' }
            steps {
                script { deployStage('staging', env.IMAGE_NAME, env.IMAGE_TAG) }
            }
        }

        stage('Approval for Production') {
            when { branch 'main' }
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    input message: 'Deploy to Production?', ok: 'Approve'
                }
            }
        }

        stage('Deploy to Production') {
            when { branch 'main' }
            steps {
                script { deployStage('prod', env.IMAGE_NAME, env.IMAGE_TAG) }
            }
        }
    }

    post {
        success { echo "Pipeline succeeded: ${env.BRANCH_NAME} -> ${env.IMAGE_TAG}" }
        failure  { echo "Pipeline failed on branch: ${env.BRANCH_NAME}" }
    }
}
