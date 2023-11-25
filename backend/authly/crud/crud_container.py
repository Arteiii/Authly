import asyncio
from authly.core.utils.log import Logger
from authly.core.utils.log import LogLevel
from authly.interface import container
from authly.models import container_model, user_model

CONTAINER_COLLECTION: str = "Container"
KEYS_COLLECTION: str = "Keys"
USER_COLLECTION: str = "Users"
APPLICATION_COLLECTION: str = "Application"


async def creat_new_container(config: container_model.ContainerConfig):
    try:
        _, config.id = await container.create_container_config(
            CONTAINER_COLLECTION, config
        )

        Logger.log(LogLevel.DEBUG, config.id, type(config.id))
        container_config = user_model.UserDB(
            id=None,
            container_id=config.id,
            container_name=config.name,
            user=[],
        )

        (
            config.key_document_id,
            config.user_document_id,
            config.application_id,
        ) = await asyncio.gather(
            container.create_container_in_collection(
                KEYS_COLLECTION, container_config
            ),
            container.create_container_in_collection(
                USER_COLLECTION, container_config
            ),
            container.create_container_in_collection(
                APPLICATION_COLLECTION, container_config
            ),
        )

        Logger.log(LogLevel.DEBUG, config)

        await container.update_container_config(CONTAINER_COLLECTION, config)

    except Exception:
        raise

    else:
        return


async def update_container(name: str):
    # todo
    pass


async def get_container(cotnainer_id: str):
    # todo
    pass
