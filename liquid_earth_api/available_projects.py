from dataclasses import asdict

import requests

from liquid_earth_api._utils import BASE_URL
from liquid_earth_api.data.schemas import AddNewSpacePostData


def get_available_projects(token: str):
    response = requests.get(
        url=f"{BASE_URL}/GetAvailableProjects",
        headers={
                "Authorization": f"{token}"
        }
    )
    if response.status_code != 200:
        # add the response to the error
        raise ValueError(f"Error getting available projects. Response: {response.reason}")
    else:
        return response.json()


def create_space(add_new_space: AddNewSpacePostData, token: str):
    response = requests.post(
        url=f"{BASE_URL}/AddNewSpace",
        json=asdict(add_new_space),
        headers={
                "Authorization": f"{token}"
        }
    )
    if response.status_code != 200:
        # add the response to the error
        raise ValueError(f"Error creating space. Response: {response.reason}")
    else:
        return response.json()