import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.PullRequests
import jetbrains.buildServer.configs.kotlin.buildFeatures.commitStatusPublisher
import jetbrains.buildServer.configs.kotlin.buildFeatures.perfmon
import jetbrains.buildServer.configs.kotlin.buildFeatures.pullRequests
import jetbrains.buildServer.configs.kotlin.buildSteps.script
import jetbrains.buildServer.configs.kotlin.projectFeatures.githubIssues
import jetbrains.buildServer.configs.kotlin.triggers.vcs

/*
The settings script is an entry point for defining a TeamCity
project hierarchy. The script should contain a single call to the
project() function with a Project instance or an init function as
an argument.

VcsRoots, BuildTypes, Templates, and subprojects can be
registered inside the project using the vcsRoot(), buildType(),
template(), and subProject() methods respectively.

To debug settings scripts in command-line, run the

    mvnDebug org.jetbrains.teamcity:teamcity-configs-maven-plugin:generate

command and attach your debugger to the port 8000.

To debug in IntelliJ Idea, open the 'Maven Projects' tool window (View
-> Tool Windows -> Maven Projects), find the generate task node
(Plugins -> teamcity-configs -> teamcity-configs:generate), the
'Debug' option is available in the context menu for the task.
*/

version = "2024.12"

project {

    buildType(TestingDev001)

    features {
        githubIssues {
            id = "PROJECT_EXT_4"
            displayName = "terranigma-solutions/liquid_earth_python_sdk"
            repositoryURL = "https://github.com/terranigma-solutions/liquid_earth_python_sdk"
            param("tokenId", "")
        }
    }
}

object TestingDev001 : BuildType({
    name = "Testing Dev 001"

    params {
        param("env.PATH_TO_WEISWEILER", "%env.TERRA_PATH_DEVOPS%/meshes/Weisweiler/")
        param("env.PATH_TO_OBJ_GALLERIES_I", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/Galleries/Solid1.obj")
        param("env.PATH_TO_OBJ_SCANS", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/Core scans Boliden/rsrbF9l2zc/model.obj")
        param("REQUIREMENT_LEVEL", "READ_MESH")
        param("env.PATH_TO_OBJ_MULTIMATERIAL_II", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/MultiMaterialObj/MultiMaterialObj.obj")
        param("env.PATH_TO_INTERPRETATION", "%env.TERRA_PATH_DEVOPS%/meshes/Seismic/Anl2-1.tif")
        param("env.PATH_TO_OBJ", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/Broadhaven_Obj/model/model.obj")
        param("env.PATH_TO_OBJ_FACE_II", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/Faces/Lapp_458_Rum_19_2_2024-02-21_0820_scan5_geoim4.obj")
        param("env.TERRA_PATH_DEVOPS", """D:\OneDrive - Terranigma Solutions GmbH/Documents - Terranigma Base/DevOps/SubsurfaceTestData/""")
        param("env.PATH_TO_OBJ_FACE_I", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/Faces/face1.obj")
        param("env.PATH_TO_SEISMIC_FINAL", "%env.TERRA_PATH_DEVOPS%/meshes/Seismic/L1_final-mig.sgy")
        param("env.PATH_TO_GLB", "%env.TERRA_PATH_DEVOPS%/meshes/GLB - GLTF/Duck.glb")
        param("env.PATH_TO_SEISMIC", "%env.TERRA_PATH_DEVOPS%/meshes/Seismic/Linie01.segy")
        param("env.PATH_TO_MAGNETIC_INTERPRETATION", "%env.TERRA_PATH_DEVOPS%/meshes/Magnetic/Plate 2a - Profile 1 2D inversion.pdf")
        param("env.MPLBACKEND", "Agg")
        param("env.PATH_TO_BOLIDEN", "%env.TERRA_PATH_DEVOPS%/combined/Leapfrog_OMF/Garpenberg_global_20220715.omf")
        param("env.PATH_TO_ASCII_DRILLHOLES", "%env.TERRA_PATH_DEVOPS%/boreholes/ASCII_drillholes/")
        param("env.PATH_TO_SECTION", "%env.TERRA_PATH_DEVOPS%/meshes/Seismic/L1_CDP-Coords.txt")
        param("env.PATH_TO_GLB_COMPLEX", "%env.TERRA_PATH_DEVOPS%/meshes/GLB - GLTF/GlbFile.glb")
        param("env.PATH_TO_MTL", "%env.TERRA_PATH_DEVOPS%/meshes/OBJ/Broadhaven_Obj/model/model.mtl")
        param("env.PATH_TO_OMF", "%env.TERRA_PATH_DEVOPS%/combined/Leapfrog_OMF/Collinstown.omf")
    }

    vcs {
        root(DslContext.settingsRoot)
    }

    steps {
        script {
            name = "Setup"
            id = "Setup"
            scriptContent = """
                @echo on
                python -m venv venv
                call venv\Scripts\activate
                venv\Scripts\python -m pip install --upgrade pip
                
                echo Checking directory...
                dir
                dir .requirements
                
                venv\Scripts\pip install --verbose -r requirements/requirements.txt
                venv\Scripts\pip install --verbose teamcity-messages
            """.trimIndent()
        }
        script {
            name = "Run Test: Core"
            id = "Run_Test"
            scriptContent = """
                @echo on
                venv\Scripts\python -m pytest --teamcity -v
            """.trimIndent()
        }
        script {
            name = "Run Test: Mesh"
            id = "Run_Test_2"
            enabled = false
            executionMode = BuildStep.ExecutionMode.RUN_ON_FAILURE
            scriptContent = """
                venv\Scripts\pip install --verbose -r requirements/requirements_mesh.txt
                
                @echo on
                set REQUIREMENT_LEVEL=READ_MESH
                echo REQUIREMENT_LEVEL is %REQUIREMENT_LEVEL%
                venv\Scripts\python -m pytest --teamcity -v -m read_mesh
            """.trimIndent()
        }
    }

    triggers {
        vcs {
            branchFilter = """
                +pr: draft=false
                -:refs/heads/main
                -:<default>
            """.trimIndent()
        }
    }

    features {
        perfmon {
        }
        commitStatusPublisher {
            vcsRootExtId = "${DslContext.settingsRoot.id}"
            publisher = github {
                githubUrl = "https://api.github.com"
                authType = personalToken {
                    token = "credentialsJSON:4df4bdb0-1278-4834-a702-18ae3a286003"
                }
            }
        }
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
})
