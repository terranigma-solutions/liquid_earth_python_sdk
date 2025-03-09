package patches.buildTypes

import jetbrains.buildServer.configs.kotlin.*
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
    }
}
