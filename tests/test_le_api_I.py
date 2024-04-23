from dotenv import dotenv_values

from liquid_earth_api.data.schemas import AddDataPostData, AddNewSpacePostData
from liquid_earth_api.api import le_api, utils_api

config = dotenv_values()
user_token = config.get('TOKEN')

space_name = "Test upload from python2"


def test_get_available_projects():
    available_projects = le_api.get_available_projects(
        token=user_token
    )
    return len(available_projects)


def test_get_deeplink():
    _project: AddDataPostData = _get_test_project(space_name)

    deep_link = le_api.get_deep_link(
        post_data=_project,
        token=user_token
    )
    print(deep_link)


def test_new_space():
    data = AddNewSpacePostData(spaceName=space_name)
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
        post_data=_get_test_project(space_name),
        token=user_token
    )
    pass


def _get_test_project(space_name: str) -> AddDataPostData:
    all_projects = le_api.get_available_projects(
        token=user_token
    )
    found_project = utils_api.find_space_item(all_projects, space_name)
    post_data = AddDataPostData(
        spaceId=found_project["spaceId"],
        ownerId=found_project["ownerId"],
        dataType="static_mesh",
        fileName="test"
    )
    return post_data
