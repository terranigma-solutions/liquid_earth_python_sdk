from dotenv import dotenv_values

from liquid_earth_api.data.schemas import PostData
from gempy.core.data.enumerators import ExampleModel
from liquid_earth_api.upload_files import push_data_to_le_space
from liquid_earth_api.links import get_deep_link
from liquid_earth_api.available_projects import get_available_projects
import gempy as gp
import dotenv

config = dotenv_values()
user_token = config.get('TOKEN')


def test_get_available_projects():
    available_projects = get_available_projects(
        token=user_token
    )
    return available_projects


def test_get_deeplink():
    clashach_project: PostData = _get_clashach_project()

    deep_link = get_deep_link(
        post_data=clashach_project,
        token=user_token
    )
    print(deep_link)


def test_upload_data_to_space():
    # * Getting available projects
    foo = push_data_to_le_space(
        geo_model=gp.generate_example_model(ExampleModel.ANTICLINE, compute_model=True),
        post_data=_get_test_project(),
        token=user_token
    )


def _get_clashach_project() -> PostData:
    all_projects = test_get_available_projects()
    # Look for the item that the ["name"] == "Clashach"
    for project in all_projects:
        if project["name"] == "Clashach":
            clashach_project = project
    if clashach_project is None:
        raise ValueError("Clashach project not found")
    post_data = PostData(
        spaceId=clashach_project["spaceId"],
        ownerId=clashach_project["ownerId"],
        dataType="static_mesh",
        fileName="test"
    )
    return post_data


def _get_test_project() -> PostData:
    all_projects = test_get_available_projects()
    # Look for the item that the ["name"] == "Clashach"
    for project in all_projects:
        if project["name"] == "Test upload":
            found_project = project
    if found_project is None:
        raise ValueError("project not found")
    post_data = PostData(
        spaceId=found_project["spaceId"],
        ownerId=found_project["ownerId"],
        dataType="static_mesh",
        fileName="test"
    )
    return post_data
