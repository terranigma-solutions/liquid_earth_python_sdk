from io import BytesIO

from azure.storage.blob import BlobClient

import subsurface


def push_unstructured_data(unstructured_data: subsurface.UnstructuredData, sas_dict: dict):
    meshes = unstructured_data
    try:
        data = meshes.to_binary()
        blob_client = BlobClient.from_blob_url(sas_dict["sasForTestLe"])
        stream = BytesIO(data)
        val = blob_client.upload_blob(
            stream,
            blob_type="BlockBlob",
            overwrite=True
        )
        print(f"Uploaded file: {val}")
        return True
    except Exception as e:
        print(f"Error uploading files: {e}")
        raise ValueError(f"Error uploading files: {e}")


