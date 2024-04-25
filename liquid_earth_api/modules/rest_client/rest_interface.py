from liquid_earth_api.modules.rest_client._utils import BASE_URL, handle_response
from liquid_earth_api.data.schemas import AddNewSpacePostData, AddDataPostData
import requests
from dataclasses import asdict


def get_deep_link(post_data: AddDataPostData, token: str) -> dict:
    response = requests.post(
        url=f"{BASE_URL}/GetDeepLinkFromSpace",
        json=asdict(post_data),
        headers={"Authorization": f"{token}"}
    )
    return handle_response(response)  # Use helper to process the response


def post_add_data_to_space(post_data: AddDataPostData, token: str) -> dict:
    response = requests.post(
        url=f"{BASE_URL}/AddDataToSpace",
        json=asdict(post_data),
        headers={"Authorization": f"{token}"}
    )
    return handle_response(response)


def get_available_projects(token: str) -> list:
    response = requests.get(
        url=f"{BASE_URL}/GetAvailableProjects",
        headers={"Authorization": f"{token}"}
    )
    return handle_response(response)


def post_create_space(add_new_space: AddNewSpacePostData, token: str) -> dict:
    response = requests.post(
        url=f"{BASE_URL}/AddNewSpace",
        json=asdict(add_new_space),
        headers={"Authorization": f"{token}"}
    )
    return handle_response(response)
