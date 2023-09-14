import json

import requests
from azure.storage.blob import BlobClient
import gempy as gp
import subsurface as ss


def push_data_to_le_space(geo_model: gp.data.GeoModel):
    # response = requests.get("http://localhost:7071/api/AddDataToSpace")
    if True:
      _push_binaries(geo_model)


def _push_binaries(geo_model):
    # response = requests.get("http://localhost:7071/api/AddDataToSpace")
    sas_dict = {
        "sasForTestLe": "https://leprojectsdata.blob.core.windows.net/74d3edaeaf0d406a81d867d3a3df0c4e/static_mesh%5Ctest.le?sv=2023-08-03&se=2023-09-14T15%3A31%3A26Z&sr=b&sp=w&sig=fgNaewJjMjzNYJ%2Ff3pAP4Vut%2FydeIgoyxy8JyZXDOZE%3D",
        "sasForTestJson": "https://leprojectsdata.blob.core.windows.net/74d3edaeaf0d406a81d867d3a3df0c4e/static_mesh%5Ctest.json?sv=2023-08-03&se=2023-09-14T15%3A31%3A26Z&sr=b&sp=w&sig=whBnknPM0ILm2XqDryW6SRO8IaeEgjn1e1t9DE8%2Bdyc%3D"
    }
    sas = "https://leprojectsdata.blob.core.windows.net/74d3edaeaf0d406a81d867d3a3df0c4e/static_mesh%5Ctest?sv=2023-08-03&se=2023-09-14T15%3A02%3A56Z&sr=b&sp=w&sig=RnbPEupD36MSgMIqvBIAJ8WiaXVKQX6GDmlNeKkNQXI%3D"
    meshes: ss.UnstructuredData = geo_model.solutions.raw_arrays.meshes_to_subsurface()
    data, header = meshes.to_binary()
    blob_client = BlobClient.from_blob_url(sas_dict["sasForTestLe"])
    response = blob_client.upload_blob(data, overwrite=True)
    blob_client = BlobClient.from_blob_url(sas_dict["sasForTestJson"])
    response = blob_client.upload_blob(json.dumps(header), overwrite=True)
    print(response)
