package patches.buildTypes

import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.PullRequests
import jetbrains.buildServer.configs.kotlin.buildFeatures.pullRequests
import jetbrains.buildServer.configs.kotlin.ui.*

/*
This patch script was generated by TeamCity on settings change in UI.
To apply the patch, change the buildType with id = 'TestingDev001'
accordingly, and delete the patch script.
*/
changeBuildType(RelativeId("TestingDev001")) {
    params {
        expect {
            param("env.LIQUID_EARTH_API_TOKEN_DEV001", "credentialsJSON:ApiToken_Dev001")
        }
        update {
            password("env.LIQUID_EARTH_API_TOKEN_DEV001", "credentialsJSON:e740f821-25ac-410c-9f81-2b8cb7c7911e")
        }
        expect {
            param("env.LIQUID_EARTH_API_TOKEN_LEGACY", "credentialsJSON:ApiToken_Legacy")
        }
        update {
            password("env.LIQUID_EARTH_API_TOKEN_LEGACY", "credentialsJSON:e740f821-25ac-410c-9f81-2b8cb7c7911e")
        }
        expect {
            param("env.LIQUID_EARTH_API_TOKEN_REVEAL", "credentialsJSON:ApiToken_Reveal")
        }
        update {
            password("env.LIQUID_EARTH_API_TOKEN_REVEAL", "credentialsJSON:d14b7073-3cd7-4e10-a829-2a094b2576a8")
        }
        expect {
            param("env.LOGIN_PASSWORD", "credentialsJSON:LoginPassword")
        }
        update {
            password("env.LOGIN_PASSWORD", "credentialsJSON:d61e0721-071f-4838-9940-145fe0709afd")
        }
        expect {
            param("env.LOGIN_SUBSCRIPTION_KEY", "credentialsJSON:SubscriptionKey")
        }
        update {
            param("env.LOGIN_SUBSCRIPTION_KEY", "0d7113b9f2054be8b4e1b350f18a7f72")
        }
        expect {
            param("env.LOGIN_USER", "credentialsJSON:LoginUser")
        }
        update {
            param("env.LOGIN_USER", "miguel@terranigma-solutions.com")
        }
        expect {
            param("env.TEST_LOGIN_TOKEN", "credentialsJSON:TestLoginToken")
        }
        update {
            param("env.TEST_LOGIN_TOKEN", "Not sure how to set this yet")
        }
        add {
            param("env.TERRA_PATH_DEVOPS", "Not set")
        }
    }

    features {
        val feature1 = find<PullRequests> {
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
        feature1.apply {
            provider = github {
                serverUrl = ""
                authType = token {
                    token = "credentialsJSON:4df4bdb0-1278-4834-a702-18ae3a286003"
                }
                filterSourceBranch = ""
                filterTargetBranch = ""
                filterAuthorRole = PullRequests.GitHubRoleFilter.MEMBER
                ignoreDrafts = true
            }
        }
    }
}
