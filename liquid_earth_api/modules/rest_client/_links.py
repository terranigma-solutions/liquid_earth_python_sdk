from dataclasses import asdict

import requests

from liquid_earth_api.modules.rest_client._utils import BASE_URL
from liquid_earth_api.data.schemas import AddDataPostData


def get_deep_link(post_data: AddDataPostData, token: str):
    response = requests.post(
        url=f"{BASE_URL}/GetDeepLinkFromSpace",
        json=asdict(post_data),
        headers={
                "Authorization": f"{token}"
        }
    )

    # if request 200 return the deep link from text/plain
    if response.status_code == 200:
        return response.text
    else:
        print("Error getting deep link")
        return False
