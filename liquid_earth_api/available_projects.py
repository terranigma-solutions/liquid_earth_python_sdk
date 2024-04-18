import requests

from liquid_earth_api._utils import BASE_URL


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
