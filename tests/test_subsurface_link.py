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

    path = os.environ.get("PATH_TO_DXF_DATA_PATH_SMALL")
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
        # space_name="Demo (exported from geoh5)",
        space_name="Shared Example: MX",
        data=unstruct,
        file_name="dxf",
        token=user_token,
        grab_link=False
    )
    pass


def test_mx_mesh_to_existing_space():
    import subsurface as ss
    from subsurface.modules.reader.mesh.mx_reader import mx_to_unstruct_from_file
    unstruct: ss.UnstructuredData = mx_to_unstruct_from_file(os.getenv("PATH_TO_MX"))

    ts = ss.TriSurf(mesh=unstruct)
    s = ss.visualization.to_pyvista_mesh(ts)
    ss.visualization.pv_plot([s], image_2d=True)

    new_file = open(f"mx.le", "wb")
    new_file.write(unstruct.to_binary())

    link = le_api.upload_mesh_to_existing_space(
        space_name="Shared Example: MX",
        data=unstruct,
        file_name="mx_file.le",
        token=user_token
    )
    pass
