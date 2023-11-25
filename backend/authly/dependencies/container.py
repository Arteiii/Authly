from authly.api.api_v2 import http_exceptions
from authly.crud.crud_container import CONTAINER_COLLECTION
from authly.interface.container import get_container_data
from authly.models.container_model import ContainerConfig
from bson import ObjectId


async def get_container_config(container_id: str) -> ContainerConfig:
    try:
        object_id = ObjectId(container_id)

        status, data = await get_container_data(
            CONTAINER_COLLECTION, object_id
        )
        if status:
            return data
        raise http_exceptions.container_id_not_found

    except Exception:
        # Handle the InvalidId exception
        raise http_exceptions.invalid_document_id
