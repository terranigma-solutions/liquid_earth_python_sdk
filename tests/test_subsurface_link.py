import os

from dotenv import load_dotenv

from liquid_earth_api.api import le_api

load_dotenv()

user_token = os.environ.get("LIQUID_EARTH_API_TOKEN")

space_name = "Ideon demo space"

def test_dxf_mesh_to_existing_space():
    import subsurface as ss
    from subsurface.modules.reader import dxf_file_to_unstruct_input
    import pandas 
    
    path = os.environ.get("DXF_DATA_PATH")
    vertex, cells, cell_attr_int, cell_attr_map = dxf_file_to_unstruct_input(path)

    unstruct = ss.UnstructuredData.from_array(
        vertex,
        cells,
        cells_attr=pandas.DataFrame(cell_attr_int, columns=["Id"]),
        xarray_attributes={"cell_attr_map": cell_attr_map},
    )

    ts = ss.TriSurf(mesh=unstruct)
    s = ss.visualization.to_pyvista_mesh(ts)
    if False:
        ss.visualization.pv_plot([s], image_2d=False)

    link = le_api.upload_mesh_to_existing_space(
        space_name="Ideon Demo (exported from geoh5)",
        data=unstruct,
        file_name="upc_surface_api",
        token=user_token
    )
    #'https://reveal-earth.app.link/1067130d-29ec-4daa-b6e4-b23d833fa625'
    pass

