import json
from dataclasses import asdict

import requests
from azure.storage.blob import BlobClient

import gempy as gp
import subsurface as ss
from liquid_earth_api.modules.client._utils import BASE_URL
from liquid_earth_api.data.schemas import AddDataPostData


def push_data_to_le_space(geo_model: gp.data.GeoModel, post_data: AddDataPostData, token: str):
    response = requests.post(
        url=f"{BASE_URL}/AddDataToSpace",
        json=asdict(post_data),
        headers={
                "Authorization": f"{token}"
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
