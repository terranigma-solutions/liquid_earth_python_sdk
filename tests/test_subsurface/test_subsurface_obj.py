import os

import pytest

import subsurface as ss
from liquid_earth_sdk.core.output import ServerResponse

from subsurface.modules.reader.mesh._trimesh_reader import _load_with_trimesh
from liquid_earth_sdk.api import le_api

ONLY_EXPLICIT = True

@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_obj_one_element_no_texture():
    path_to_obj = os.getenv("TERRA_PATH_DEVOPS") + "/meshes/OBJ/TexturedMesh/PenguinBaseMesh.obj"
    trimesh_obj = _load_with_trimesh(
        path_to_obj=path_to_obj,
        plot=False
    )
    ts: ss.TriSurf = ss.modules.reader.mesh._trimesh_reader.trimesh_to_unstruct(trimesh_obj)

    if False:
        s = ss.visualization.to_pyvista_mesh(ts)
        ss.visualization.pv_plot([s], image_2d=False)

    if True:
        unstruct: ss.UnstructuredData = ts.mesh
        response: ServerResponse = le_api.upload_mesh_to_new_space(
            space_name="[TEMP] Test PythonSDk: OBJ one element no texture",
            data=unstruct,
            file_name="obj_one_element_no_texture",
            token=(os.environ.get("LIQUID_EARTH_API_TOKEN")),
            grab_link=False
        )
        
        pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_OBJ_trimesh_THREE_ELEMENTS_no_texture_to_unstruct():
    pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_OBJ_ONE_element_texture_to_unstruct():
    pass


@pytest.mark.skipif(ONLY_EXPLICIT, reason="Run Explicit")
def test_OBJ_three_element_texture_to_unstruct():
    pass
