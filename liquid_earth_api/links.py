from dataclasses import asdict

import requests

from liquid_earth_api._utils import BASE_URL
from liquid_earth_api.data.schemas import PostData


def get_deep_link(post_data: PostData, token: str):
    response = requests.post(
        url=f"{BASE_URL}/GetDeepLinkFromSpace",
        json=asdict(post_data),
        headers={
                "Authorization": f"Bearer {token}"
        }
    )

    # if request 200 return the deep link from text/plain
    if response.status_code == 200:
        return response.text
    else:
        print("Error getting deep link")
        return False
