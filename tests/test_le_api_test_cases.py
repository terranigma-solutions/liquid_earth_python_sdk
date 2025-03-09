import os
import pytest
from dotenv import load_dotenv
from liquid_earth_api.data.schemas import AddDataPostData, AddNewSpacePostData
from liquid_earth_api.api import le_api, utils_api

load_dotenv()


@pytest.mark.core
class TestLEApiBase:
    """Base test class with common setup"""

    @classmethod
    def setup_class(cls):
        cls.user_token = os.environ.get("LIQUID_EARTH_API_TOKEN")
        cls.space_name = "[TEMP] Test python api"

    def _get_test_project(self, space_name: str) -> AddDataPostData:
        all_projects = le_api.get_available_projects(
            token=self.user_token
        )
        found_project = utils_api.find_space_item(all_projects, space_name)
        post_data = AddDataPostData(
            spaceId=found_project["SpaceId"],
            ownerId=found_project["OwnerId"],
            dataType="static_mesh",
            fileName="test"
        )
        return post_data


class TestLEApiNoGempy(TestLEApiBase):
    """Tests that don't require GemPy"""

    def test_get_available_projects(self):
        available_projects = le_api.get_available_projects(
            token=self.user_token
        )
        assert len(available_projects) > 0


    @pytest.mark.skip("not ready")
    def test_new_space(self):
        data = AddNewSpacePostData(spaceName=self.space_name)
        response = le_api.post_create_space(
            add_new_space=data,
            token=self.user_token
        )
        assert response is not None

    @pytest.mark.skip("not ready")
    def test_get_deeplink(self):
        _project: AddDataPostData = self._get_test_project(self.space_name)
        deep_link = le_api.get_deep_link(
            post_data=_project,
            token=self.user_token
        )
        assert deep_link is not None
        

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