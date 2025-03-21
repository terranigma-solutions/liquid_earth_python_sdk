package patches.buildTypes

import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.BuildType
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.triggers.vcs
import jetbrains.buildServer.configs.kotlin.ui.*

/*
This patch script was generated by TeamCity on settings change in UI.
To apply the patch, create a buildType with id = 'Release'
in the root project, and delete the patch script.
*/
create(DslContext.projectId, BuildType({
    id("Release")
    name = "Release"

    params {
        param("env.PACKAGE_VERSION", "")
    }

    vcs {
        root(RelativeId("HttpsGithubComTerranigmaSolutionsLiquidEarthPythonSdkRefsHeadsMain1"))
    }

    steps {
        script {
            name = "Git Tagging"
            id = "Git_Tagging"
            scriptContent = """
                git config user.name "TeamCity Bot"
                git config user.email "ci@terraniga-solutions.com"
                git tag %env.PACKAGE_VERSION%
                git push origin %env.PACKAGE_VERSION%
            """.trimIndent()
        }
        script {
            name = "Build"
            id = "Build"
            scriptContent = """
                python -m pip install --upgrade build
                python -m build
            """.trimIndent()
        }
        script {
            name = "Push to PyPi"
            id = "Push_to_PyPi"
            scriptContent = """
                python -m pip install --upgrade twine
                python -m twine upload dist/* -u __token__ -p %env.TWINE_PASSWORD%
            """.trimIndent()
        }
    }

    triggers {
        vcs {
            enabled = false
        }
    }

    features {
        perfmon {
        }
    }
}))

