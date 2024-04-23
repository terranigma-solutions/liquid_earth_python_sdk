from dotenv import dotenv_values

from liquid_earth_api.data.schemas import AddDataPostData, AddNewSpacePostData
from liquid_earth_api.api import le_api

config = dotenv_values()
user_token = config.get('TOKEN')


def test_get_available_projects():
    available_projects = le_api.get_available_projects(
        token=user_token
    )
    return available_projects


def test_get_deeplink():
    _project: AddDataPostData = _get_test_project("Test upload from python")

    deep_link = le_api.get_deep_link(
        post_data=_project,
        token=user_token
    )
    print(deep_link)


def test_new_space():
    data = AddNewSpacePostData(spaceName="Test upload from python")
    bar = le_api.post_create_space(
        add_new_space=data,
        token=user_token
    )
    
    print(bar)


def test_upload_data_to_space():
    # * Getting available projects
    import gempy as gp
    from gempy.core.data.enumerators import ExampleModel
    
    foo = le_api.post_add_data_to_space(
        geo_model=gp.generate_example_model(ExampleModel.ANTICLINE, compute_model=True),
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
