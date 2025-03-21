from io import BytesIO
from typing import Any, Dict

from azure.storage.blob import BlobClient

import subsurface

from io import BytesIO
from typing import Dict, Any
from azure.storage.blob import BlobClient
import logging


def push_unstructured_data(unstructured_data: 'subsurface.UnstructuredData', sas_dict: Dict[str, str]) -> bool:
    """
    Upload unstructured data to Azure Blob Storage.
    
    Args:
        unstructured_data: The unstructured data to be uploaded
        sas_dict: Dictionary containing SAS tokens for blob storage access
        
    Returns:
        bool: True if upload was successful
        
    Raises:
        ValueError: If there's an error during upload
    """
    logger = logging.getLogger(__name__)

    if not sas_dict.get("sasForTestLe"):
        raise ValueError("Missing required SAS token in sas_dict")

    try:
        # Convert data to binary
        binary_data = unstructured_data.to_binary()

        # Initialize blob client and create data stream
        blob_client = BlobClient.from_blob_url(sas_dict["sasForTestLe"])
        data_stream = BytesIO(binary_data)

        # Upload data to blob storage
        upload_result = blob_client.upload_blob(
            data_stream,
            blob_type="BlockBlob",
            overwrite=True
        )

        logger.info(f"Successfully uploaded blob: {upload_result}")
        return True

    except Exception as e:
        error_message = f"Error uploading data to blob storage: {str(e)}"
        logger.error(error_message)
        raise ValueError(error_message) from e
