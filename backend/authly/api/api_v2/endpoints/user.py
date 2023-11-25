from authly.crud import crud_user
from authly.dependencies.container import get_container_config
from authly.models.container_model import ContainerConfig
from fastapi import APIRouter, Depends


user = APIRouter()


@user.get("/{container_id}/")
async def user_router_hello_world(
    container_id: str, config: ContainerConfig = Depends(get_container_config)
):
    return {
        "msg": f"Hello World from container with id: {config.id}",
        "name": config.name,
    }


@user.post("/create/{container_id}")
async def create_user(config: ContainerConfig = Depends(get_container_config)):
    result = await crud_user.create_new_user(config.user_document_id, )
