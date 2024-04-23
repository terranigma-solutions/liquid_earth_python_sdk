from typing import Union

import gempy
from ..data.schemas import AddDataPostData, AddNewSpacePostData
from ..modules.rest_client import rest_interface
from ..modules.blob_client import blob_interface


def get_deep_link(post_data: AddDataPostData, token: str):
    response = rest_interface.get_deep_link(post_data, token)
    print(response.text)


def get_available_projects(token: str):
    return rest_interface.get_available_projects(token)


def post_create_space(add_new_space: AddNewSpacePostData, token: str) -> dict:
    return rest_interface.post_create_space(add_new_space, token)


def post_add_data_to_space(geo_model: gempy.data.GeoModel, post_data: AddDataPostData, token: str):
    response: dict = rest_interface.post_add_data_to_space(post_data, token)
    uploading_files_response = blob_interface.push_unstructured_data(
        unstructured_data=geo_model.solutions.raw_arrays.meshes_to_subsurface(),
        sas_dict=response
    )
    print(uploading_files_response.text)
    return uploading_files_response
