import asyncio
from authly.core.utils.log import Logger
from authly.core.utils.log import LogLevel
from authly.interface import bubble
from authly.models import bubble_model, user_model

BUBBLES_COLLECTION: str = "Bubbles"
KEYS_COLLECTION: str = "Keys"
USERS_COLLECTION: str = "Users"
APPLICATIONS_COLLECTION: str = "Applications"


async def creat_new_bubble(
    create: bubble_model.CreateBubble,
) -> bubble_model.BubbleConfig:
    try:
        result = bubble_model.BubbleConfig
        result.name = create.name

        _, result.id = await bubble.create_bubble_config(
            BUBBLES_COLLECTION, create
        )

        Logger.log(LogLevel.DEBUG, result.id, type(result.id))
        bubble_config = user_model.UserDB(
            id=None,
            bubble_id=result.id,
            bubble_name=result.name,
            user=[],
        )

        (
            result.key_document_id,
            result.user_document_id,
            result.application_id,
        ) = await asyncio.gather(
            bubble.create_bubble_in_collection(KEYS_COLLECTION, bubble_config),
            bubble.create_bubble_in_collection(
                USERS_COLLECTION, bubble_config
            ),
            bubble.create_bubble_in_collection(
                APPLICATIONS_COLLECTION, bubble_config
            ),
        )

        Logger.log(LogLevel.DEBUG, result)

        await bubble.update_bubble_config(
            collection_name=BUBBLES_COLLECTION,
            config=result,
        )

    except Exception:
        raise

    else:
        return result


async def update_bubble():
    # todo
    pass


async def get_bubble(bubble_id: str):
    # todo
    pass


async def delete_bubble(bubble_id: str):
    try:
        _, config.id = await bubble.create_bubble_config(
            BUBBLES_COLLECTION, config
        )

        Logger.log(LogLevel.DEBUG, config.id, type(config.id))
        bubble_config = user_model.UserDB(
            id=None,
            bubble_id=config.id,
            bubble_name=config.name,
            user=[],
        )

        (
            config.key_document_id,
            config.user_document_id,
            config.application_id,
        ) = await asyncio.gather(
            bubble.create_bubble_in_collection(KEYS_COLLECTION, bubble_config),
            bubble.create_bubble_in_collection(
                USERS_COLLECTION, bubble_config
            ),
            bubble.create_bubble_in_collection(
                APPLICATIONS_COLLECTION, bubble_config
            ),
        )

        Logger.log(LogLevel.DEBUG, config)

        await bubble.update_bubble_config(BUBBLES_COLLECTION, config)

    except Exception:
        raise

    else:
        return True
