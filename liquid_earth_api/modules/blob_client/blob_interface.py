import json

from azure.storage.blob import BlobClient

import subsurface


def push_unstructured_data(unstructured_data: subsurface.UnstructuredData, sas_dict: dict):
    meshes = unstructured_data
    try:
        data, header = meshes.to_binary()
        blob_client = BlobClient.from_blob_url(sas_dict["sasForTestLe"])
        response = blob_client.upload_blob(data, overwrite=True)
        blob_client = BlobClient.from_blob_url(sas_dict["sasForTestJson"])
        response = blob_client.upload_blob(json.dumps(header), overwrite=True)
        return response
    except Exception as e:
        print(f"Error uploading files: {e}")
        ValueError("Error uploading files")
        
