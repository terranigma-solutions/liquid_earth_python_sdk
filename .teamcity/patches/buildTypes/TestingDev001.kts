package patches.buildTypes

import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.CommitStatusPublisher
import jetbrains.buildServer.configs.kotlin.buildFeatures.PullRequests
import jetbrains.buildServer.configs.kotlin.buildFeatures.commitStatusPublisher
import jetbrains.buildServer.configs.kotlin.buildFeatures.pullRequests
import jetbrains.buildServer.configs.kotlin.triggers.VcsTrigger
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import jetbrains.buildServer.configs.kotlin.ui.*

/*
This patch script was generated by TeamCity on settings change in UI.
To apply the patch, change the buildType with id = 'TestingDev001'
accordingly, and delete the patch script.
*/
changeBuildType(RelativeId("TestingDev001")) {
    params {
        expect {
            param("env.PATH_TO_MX", "%env.TERRA_PATH_DEVOPS%/volume/GOCAD/mix/horizons_faults.mx")
        }
        update {
            param("env.PATH_TO_MX", "%env.TERRA_PATH_DEVOPS%/meshes/GOCAD/mix/horizons_faults_small.mx")
        }
        expect {
            param("env.TERRA_PATH_DEVOPS", "Not set")
        }
        update {
            param("env.TERRA_PATH_DEVOPS", "D:/OneDrive - Terranigma Solutions GmbH/Documents - Terranigma Base/DevOps/SubsurfaceTestData/")
        }
    }

    triggers {
        val trigger1 = find<VcsTrigger> {
            vcs {
                branchFilter = """
                    +pr: draft=false
                    -:refs/heads/main
                    -:<default>
                """.trimIndent()
            }
        }
        trigger1.apply {
            branchFilter = """
                +pr:draft=false
                +:<default>
            """.trimIndent()

        }
    }

    features {
        val feature1 = find<CommitStatusPublisher> {
            commitStatusPublisher {
                vcsRootExtId = "${DslContext.settingsRoot.id}"
                publisher = github {
                    githubUrl = "https://api.github.com"
                    authType = personalToken {
                        token = "credentialsJSON:4df4bdb0-1278-4834-a702-18ae3a286003"
                    }
                }
            }
        }
        feature1.apply {
            vcsRootExtId = ""
        }
        val feature2 = find<PullRequests> {
            pullRequests {
                vcsRootExtId = "${DslContext.settingsRoot.id}"
                provider = github {
                    authType = token {
                        token = "credentialsJSON:4df4bdb0-1278-4834-a702-18ae3a286003"
                    }
                    filterAuthorRole = PullRequests.GitHubRoleFilter.MEMBER
                }
            }
        }
        feature2.apply {
            vcsRootExtId = ""
        }
    }
}
