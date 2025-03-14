import os
import pytest
from dotenv import load_dotenv
from liquid_earth_api.data.schemas import AddDataPostData, AddNewSpacePostData, DeleteSpacePostData
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


class TestLEApiCore(TestLEApiBase):

    def test_get_available_projects(self):
        available_projects = le_api.get_available_projects(
            token=self.user_token
        )
        assert len(available_projects) > 0


    def test_new_space_get_link_delete_space(self):
        response = le_api.post_create_space(
            add_new_space=(AddNewSpacePostData(spaceName=self.space_name)),
            token=self.user_token
        )
        assert response is not None

        _project: AddDataPostData = self._get_test_project(self.space_name)
        deep_link = le_api.get_deep_link(
            post_data=_project,
            token=self.user_token
        )
        assert deep_link is not None

        response = le_api.delete_space(
            delete_space_post_data=DeleteSpacePostData(spaceId=_project.spaceId),
            token=self.user_token
        )
        
        assert response is not None
        

