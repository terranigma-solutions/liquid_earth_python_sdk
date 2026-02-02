import os
import pytest
import numpy as np
import subsurface
from dotenv import load_dotenv
from liquid_earth_sdk.core.data.schemas import AddDataPostData, AddNewSpacePostData, DeleteSpacePostData
from liquid_earth_sdk.api import le_api, _utils_api
from liquid_earth_sdk.core.output import AvailableProject, ServerResponse
from liquid_earth_sdk.modules.rest_client import rest_interface

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
        found_project = _utils_api.find_space_item(all_projects, space_name)
        post_data = AddDataPostData(
            spaceId=found_project["SpaceId"],
            ownerId=found_project["OwnerId"],
            dataType="static_mesh",
            fileName="test"
        )
        return post_data


class TestLEApiCore(TestLEApiBase):

    def test_get_available_projects(self):
        available_projects: list[AvailableProject] = le_api.get_available_projects(
            token=self.user_token
        )
        assert len(available_projects) > 0

    def test_new_space_get_link_delete_space(self):
        space = (AddNewSpacePostData(spaceName=self.space_name))
        response = rest_interface.post_create_space(space, self.user_token)
        assert response is not None

        # ! Here we are not uploading the binary that would be the normal process

        all_projects = le_api.get_available_projects(
            token=self.user_token
        )
        found_project: AvailableProject = _utils_api.find_space_item(all_projects, self.space_name)
        post_data = AddDataPostData(
            spaceId=found_project.SpaceId,
            ownerId=found_project.OwnerId,
            dataType="static_mesh",
            fileName="test",
            texture_ext=None
        )
        deep_link = le_api.get_deep_link(
            post_data=post_data,
            token=self.user_token
        )
        assert deep_link is not None

        response = le_api.delete_space(
            delete_space_post_data=DeleteSpacePostData(spaceId=post_data.spaceId),
            token=self.user_token
        )

        assert response is not None

    def test_upload_volume_to_new_space(self):
        # Create a mock subsurface.StructuredData with 10x10x10 random numbers between 0.0 and 10.0
        data = np.random.uniform(0.0, 10.0, (10, 10, 10))
        sd = subsurface.StructuredData.from_numpy(data)

        # Upload volume to new space
        # Note: This will actually call the API if user_token is valid.
        # Given the existing tests in this file seem to be integration tests
        # (they use os.environ.get("LIQUID_EARTH_API_TOKEN")), I will follow that pattern.
        # If the token is missing, the test should probably be skipped or fail gracefully
        # depending on how other tests handle it.
        if not self.user_token:
            pytest.skip("LIQUID_EARTH_API_TOKEN not set")

        space_name =  "[TEMP] volume api test 3"
        server_response: ServerResponse = le_api.upload_volume_to_new_space(
            space_name=space_name,
            data=sd,
            file_name="test_volume",
            token=self.user_token
        )

        assert server_response is not None
        assert server_response.selected_project.Name == space_name
        print (server_response.selected_project.SpaceId)
        # Cleanup
      #  le_api.delete_space(
      #      delete_space_post_data=DeleteSpacePostData(spaceId=server_response.selected_project.SpaceId),
      #      token=self.user_token
      #  )
