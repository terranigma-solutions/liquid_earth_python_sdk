from typing import Union, Optional
from . import _utils_api
from liquid_earth_sdk.core.data.schemas import (
    AddDataPostData, AddNewSpacePostData, DeleteSpacePostData,
    ChangeSpaceRolePostData, ImportDataToSpacePostData, GetSpaceUpdatesPostData
)
from ..core.output import ServerResponse, AvailableProject
from ..modules.blob_client.blob_interface import valid_data_types
from ..modules.rest_client import rest_interface
from ..modules.blob_client import blob_interface

import os


def set_token(token: str):
    # Check that the first 3 characters are le-
    if token[:3] != 'le-':
        raise ValueError('The token is invalid. Generate a new token from the LiquidEarth WebApp')

    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(f'LIQUID_EARTH_TOKEN={token}\n')
    else:
        with open('.env', 'a') as f:
            f.write(f'LIQUID_EARTH_TOKEN={token}\n')


def upload_mesh_to_existing_space(space_name: str, data: valid_data_types, file_name: str,
                                  token: str, grab_link: bool = True) -> ServerResponse:

    # * Make sure file name does not contain .le
    if file_name.endswith('.le'):
        file_name = file_name[:-3]

    # * grab space
    available_projects: list[AvailableProject] = get_available_projects(token)

    # ? which type is actually returned here?a
    found_project:AvailableProject = _utils_api.find_space_item(
        all_projects=available_projects,
        space_name=space_name
    )

    link: Optional[str] = _upload_mesh_common(
        data=data,
        file_name=file_name,
        found_project=found_project,
        grab_link=grab_link,
        token=token
    )

    server_response = ServerResponse(
        deep_link=link,
        available_projects=available_projects,
        selected_project=found_project
    )

    return server_response


def upload_mesh_to_new_space(space_name: str, data: valid_data_types,
                             file_name: str, token: str, grab_link: bool = True) -> ServerResponse:
    post_data = AddNewSpacePostData(spaceName=space_name)
    new_project = rest_interface.post_create_space(post_data, token)
    available_project = AvailableProject(**new_project)
    
    link: Optional[str] = _upload_mesh_common(
        data=data,
        file_name=file_name,
        found_project=available_project,
        grab_link=grab_link,
        token=token
    )
    
    server_response = ServerResponse(
        deep_link=link,
        available_projects=[available_project],
        selected_project=available_project
    )

    return server_response


def get_deep_link(post_data: AddDataPostData, token: str) -> str:
    return rest_interface.get_deep_link(post_data, token)


def get_available_projects(token: str):
    return rest_interface.get_available_projects(token)


def delete_space(delete_space_post_data: DeleteSpacePostData, token: str) -> dict:
    return rest_interface.delete_space(delete_space_post_data, token)


def change_space_role(
    space_id: str,
    owner_id: str,
    target_email: str,
    permissions: int,
    token: str
) -> dict:
    post_data = ChangeSpaceRolePostData(
        spaceId=space_id,
        ownerId=owner_id,
        targetEmail=target_email,
        permissions=permissions
    )
    return rest_interface.change_space_role(post_data, token)


def import_data_to_space(
    space_id: str,
    owner_id: str,
    path_in: str,
    type_of_import: str,
    token: str,
    transformation: dict | None = None,
    attr_name: str | None = None,
    missing_value: float | None = None,
    band: int | None = None,
    collar_reader: dict | None = None,
    survey_reader: dict | None = None,
    attrs_reader: dict | None = None,
    is_lith_attr: bool | None = None,
    number_nodes: int | None = None,
    vertex_reader: dict | None = None,
    edges_reader: dict | None = None,
    cells_attrs_reader: dict | None = None,
    vertex_attrs_reader: dict | None = None,
    coord_reader: dict | None = None,
    interpolation_resolution: list | None = None,
    path_in_msh: str | None = None,
    path_in_mod_or_den: str | None = None,
    **kwargs
) -> dict:
    post_data = ImportDataToSpacePostData(
        spaceId=space_id,
        ownerId=owner_id,
        path_in=path_in,
        type_of_import=type_of_import,
        transformation=transformation,
        attr_name=attr_name,
        missing_value=missing_value,
        band=band,
        collar_reader=collar_reader,
        survey_reader=survey_reader,
        attrs_reader=attrs_reader,
        is_lith_attr=is_lith_attr,
        number_nodes=number_nodes,
        vertex_reader=vertex_reader,
        edges_reader=edges_reader,
        cells_attrs_reader=cells_attrs_reader,
        vertex_attrs_reader=vertex_attrs_reader,
        coord_reader=coord_reader,
        interpolation_resolution=interpolation_resolution,
        path_in_msh=path_in_msh,
        path_in_mod_or_den=path_in_mod_or_den,
        path_out=kwargs.pop("path_out", None),
    )
    return rest_interface.import_data_to_space(post_data, token)


def get_space_updates(space_id: str, token: str) -> dict:
    post_data = GetSpaceUpdatesPostData(spaceId=space_id)
    return rest_interface.get_space_updates(post_data, token)


def _upload_mesh_common(data: valid_data_types, file_name: str, found_project: AvailableProject,
                        grab_link: bool, token: str) -> Optional[str]:
    post_data: AddDataPostData = AddDataPostData(
        spaceId=found_project.SpaceId,
        ownerId=found_project.OwnerId,
        dataType="static_mesh",
        fileName=file_name,
        texture_ext="png"
    )
    sas_dict: dict[str] = rest_interface.post_add_data_to_space(post_data, token)
    if not sas_dict.get("sasForTestLe"):
        raise ValueError("Missing required SAS token in sas_dict")

    _ = blob_interface.push_unstructured_data(
        data_to_push=data,
        sas=sas_dict
    )

    # * Grab link
    if grab_link:
        link = get_deep_link(post_data, token)
    else:
        link = None

    return link
