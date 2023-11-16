import pytest
from authly.core.db.mongo_crud import MongoDBManager

# Test data
test_data = {"name": "John Doe", "age": 30, "email": "john.doe@example.com"}

# MongoDB connection details
db_url = "mongodb://localhost:27017"
db_name = "test_database"
collection_name = "test_collection"


async def clear_collection(manager: MongoDBManager):
    result = await manager.delete_manager.delete_many_documents({})
    return True, result, "Collection cleared successfully"


@pytest.fixture
def mongodb_manager():
    manager: MongoDBManager = MongoDBManager(db_url, db_name, collection_name)
    yield manager


@pytest.mark.asyncio
async def test_insert_document(mongodb_manager: MongoDBManager):
    write_manager = (
        mongodb_manager.write_manager
    )  # Access the write_manager directly
    result, document_id = await write_manager.insert_document(test_data)
    assert result is True
    assert document_id is not None


@pytest.mark.asyncio
async def test_find_one(mongodb_manager: MongoDBManager):
    await clear_collection(mongodb_manager)
    _, _ = await mongodb_manager.write_manager.insert_document(test_data)
    result, document = await mongodb_manager.read_manager.find_one(
        {"name": "John Doe"}
    )
    assert result is True
    assert document is not None


@pytest.mark.asyncio
async def test_find_many(mongodb_manager: MongoDBManager):
    await clear_collection(mongodb_manager)
    _, _ = await mongodb_manager.write_manager.insert_document(test_data)
    result, document_list = await mongodb_manager.read_manager.find_many(
        {"name": "John Doe"}
    )
    assert result is True
    assert isinstance(document_list, list)
    assert len(document_list) > 0


@pytest.mark.asyncio
async def test_update_one_document(mongodb_manager: MongoDBManager):
    await clear_collection(mongodb_manager)
    _, document_id = await mongodb_manager.write_manager.insert_document(
        test_data
    )
    result, _ = await mongodb_manager.update_manager.update_one_document(
        {"_id": document_id}, {"age": 31}
    )
    assert result is True


@pytest.mark.asyncio
async def test_replace_one_document(mongodb_manager: MongoDBManager):
    await clear_collection(mongodb_manager)
    _, document_id = await mongodb_manager.write_manager.insert_document(
        test_data
    )
    replace_data = {
        "_id": document_id,
        "name": "Jane Doe",
        "age": 25,
        "email": "jane.doe@example.com",
    }
    result, _ = await mongodb_manager.update_manager.replace_one_document(
        {"_id": document_id}, replace_data
    )
    assert result is True


@pytest.mark.asyncio
async def test_delete_document(mongodb_manager: MongoDBManager):
    await clear_collection(mongodb_manager)
    _, document_id = await mongodb_manager.write_manager.insert_document(
        test_data
    )
    result, _ = await mongodb_manager.delete_manager.delete_document(
        {"_id": document_id}
    )
    assert result is True


@pytest.mark.asyncio
async def test_delete_many_documents(mongodb_manager: MongoDBManager):
    await clear_collection(mongodb_manager)
    _, _ = await mongodb_manager.write_manager.insert_document(test_data)
    result, _ = await mongodb_manager.delete_manager.delete_many_documents(
        {"name": "John Doe"}
    )
    assert result is True


@pytest.mark.asyncio
async def test_close_connection(mongodb_manager: MongoDBManager):
    result, _ = await mongodb_manager.close_connection()
    assert result is True
