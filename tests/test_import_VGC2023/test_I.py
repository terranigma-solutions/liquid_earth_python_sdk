from gempy.core.data.enumerators import ExampleModel
from liquid_earth_api import push_data_to_le_space
import gempy as gp


def test_upload_data_to_space():

    model = gp.generate_example_model(ExampleModel.ANTICLINE, compute_model=True)
    foo = push_data_to_le_space(model)
