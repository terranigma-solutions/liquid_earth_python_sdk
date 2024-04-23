from dotenv import dotenv_values

from liquid_earth_api.data.schemas import AddDataPostData, AddNewSpacePostData
from gempy.core.data.enumerators import ExampleModel
from liquid_earth_api.modules.rest_client._upload_files import push_data_to_le_space
from liquid_earth_api.modules.rest_client._links import get_deep_link
from liquid_earth_api.modules.rest_client.rest_interface import get_available_projects, post_create_space
import gempy as gp

config = dotenv_values()
user_token = config.get('TOKEN')


def test_get_available_projects():
    available_projects = get_available_projects(
        token=user_token
    )
    return available_projects


def test_get_deeplink():
    clashach_project: AddDataPostData = _get_test_project("Test upload from python")

    deep_link = get_deep_link(
        post_data=clashach_project,
        token=user_token
    )
    print(deep_link)


def test_new_space():
    data = AddNewSpacePostData(spaceName="Test upload from python")
    bar = post_create_space(
        add_new_space=data,
        token=user_token
    )
    
    print(bar)


def test_upload_data_to_space():
    # * Getting available projects
    foo = push_data_to_le_space(
        post_data=_get_test_project("Test upload from python"),
        token=user_token
    )
    pass



def _get_test_project(space_name: str) -> AddDataPostData:
    all_projects = test_get_available_projects()
    # Look for the item that the ["name"] == "Clashach"
    for project in all_projects:
        if project["name"] == space_name:
            found_project = project
    if found_project is None:
        raise ValueError("project not found")
    post_data = AddDataPostData(
        spaceId=found_project["spaceId"],
        ownerId=found_project["ownerId"],
        dataType="static_mesh",
        fileName="test"
    )
    return post_data
