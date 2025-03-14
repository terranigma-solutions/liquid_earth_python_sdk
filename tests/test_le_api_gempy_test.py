import pytest

from liquid_earth_api.api import le_api
from test_le_api_test_cases import TestLEApiBase


@pytest.mark.skip("Requires GemPy")
class TestLEApiWithGempy(TestLEApiBase):
    """Tests that require GemPy"""

    @classmethod
    def setup_class(cls):
        super().setup_class()
        import gempy as gp
        from gempy.core.data.enumerators import ExampleModel
        cls.gempy_model = gp.generate_example_model(ExampleModel.ANTICLINE, compute_model=True)

    def test_upload_mesh_to_existing_space(self):
        response = le_api.upload_mesh_to_existing_space(
            space_name=self.space_name,
            data=self.gempy_model.solutions.raw_arrays.meshes_to_subsurface(),
            file_name="test2",
            token=self.user_token
        )
        assert response is not None

    def test_upload_mesh_to_new_space(self):
        response = le_api.upload_mesh_to_new_space(
            space_name="new_space_name",
            data=self.gempy_model.solutions.raw_arrays.meshes_to_subsurface(),
            file_name="test2",
            token=self.user_token
        )
        assert response is not None

    def test_upload_data_to_space(self):
        response = le_api.post_add_data_to_space(
            unstructured_data=self.gempy_model.solutions.raw_arrays.meshes_to_subsurface(),
            post_data=self._get_test_project(self.space_name),
            token=self.user_token
        )
        assert response is not None
