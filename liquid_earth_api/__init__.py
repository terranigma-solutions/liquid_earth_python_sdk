import json
from dataclasses import asdict

import requests
from azure.storage.blob import BlobClient
import gempy as gp
import subsurface as ss
import socket

from data.schemas import PostData

LOCAL = False  # Set to True for local development, False for server

BASE_URL = f"https://apim-liquidearth.azure-api.net/python" if not LOCAL else f"http://{socket.gethostname()}.local:7071/api"


def make_url(endpoint: str) -> str:
    return f"{BASE_URL}/{endpoint}"


def get_available_projects(token: str):
    response = requests.get(
        url=f"{BASE_URL}/GetAvailableProjects",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    if response.status_code != 200:
        # add the response to the error
        raise ValueError(f"Error getting available projects. Response: {response.reason}")
    else:
        return response.json()


def get_deep_link(post_data: PostData, token: str):
    response = requests.post(
        url = f"{BASE_URL}/GetDeepLinkFromSpace",
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


def push_data_to_le_space(geo_model: gp.data.GeoModel, post_data: PostData, token: str):
    response = requests.post(
        url=f"{BASE_URL}/AddDataToSpace",
        json=asdict(post_data),
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    # If request is 200 deserialize the json response in a dictionary
    if response.status_code == 200:
        sas_dict = response.json()
        try:
            uploading_files_response = _push_binaries(geo_model, sas_dict)
            return True
        except:
            print("Error uploading files")
            return False
    else:
        print("Error getting SAS")
        return False


def _push_binaries(geo_model, sas_dict: dict):
    meshes: ss.UnstructuredData = geo_model.solutions.raw_arrays.meshes_to_subsurface()
    data, header = meshes.to_binary()
    blob_client = BlobClient.from_blob_url(sas_dict["sasForTestLe"])
    response = blob_client.upload_blob(data, overwrite=True)
    blob_client = BlobClient.from_blob_url(sas_dict["sasForTestJson"])
    response = blob_client.upload_blob(json.dumps(header), overwrite=True)
    return response
    print(response)
