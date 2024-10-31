import os

from dotenv import dotenv_values, load_dotenv

from liquid_earth_api.data.schemas import AddDataPostData, AddNewSpacePostData
from liquid_earth_api.api import le_api, utils_api

load_dotenv()

user_token = os.environ.get("LIQUID_EARTH_API_TOKEN")

space_name = "Ideon demo space"

def test_dxf_mesh_to_existing_space():
    # Read and digest the DXF file
    
    
    return 
    foo = le_api.upload_mesh_to_existing_space(
        space_name="Ideon demo space",
        data=None,
        file_name="dxf_file",
        token=user_token
    )
    pass

