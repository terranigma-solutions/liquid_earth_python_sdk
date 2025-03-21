from subsurface import optional_requirements

from liquid_earth_api.api import le_api
from liquid_earth_api.data.schemas import DeleteSpacePostData
from .test_le_api_test_cases import TestLEApiBase


class TestLEApiWithGempy(TestLEApiBase):
    """Tests that require GemPy"""
    _space_id: str
    
    @classmethod
    def setup_class(cls):
        super().setup_class()
        import gempy as gp
        from gempy.core.data.enumerators import ExampleModel
        cls.gempy_model = gp.generate_example_model(ExampleModel.ANTICLINE, compute_model=True)
        
     
    @classmethod
    def teardown_class(cls):
        """Deletes the created space after the tests"""
        super().teardown_class()
        le_api.delete_space(
            delete_space_post_data=DeleteSpacePostData(spaceId=_project.spaceId),
            token=cls.user_token
        )
    
    def test_upload_mesh_to_existing_space(self):
        ss = optional_requirements.require_subsurface()
        subsurface: ss.UnstructuredData = self.gempy_model.solutions.raw_arrays.meshes_to_subsurface()
        name = self.space_name
        token = self.user_token
        
        response = le_api.upload_mesh_to_existing_space(
            space_name="[TEMP] Test python api",
            data=subsurface,
            file_name="anticline",
            token=token
        )
        assert response is not None

    def test_upload_mesh_to_new_space(self):
        response = le_api.upload_mesh_to_new_space(
            space_name="[TEMP] Test python api",
            data=self.gempy_model.solutions.raw_arrays.meshes_to_subsurface(),
            file_name="anticline",
            token=self.user_token
        )
        assert response is not None
