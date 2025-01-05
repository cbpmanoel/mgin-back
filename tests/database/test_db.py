import pytest
from bson import ObjectId
from pymongo.errors import ConnectionFailure, PyMongoError

@pytest.mark.asyncio
async def test_db_initialization_success(real_db, db_instance):
    """Test successful initialization of the DB class."""
    # Ensure the DB is not initialized yet
    assert not db_instance.is_initialized()

    # Initialize the DB
    await db_instance.initialize()

    # Ensure the DB is initialized
    assert db_instance.is_initialized()
    assert db_instance.client is not None
    assert db_instance.db.name == "test_db"

@pytest.mark.asyncio
async def test_db_initialization_failure():
    """Test DB initialization failure with invalid URL."""
    from src.db import DBConnection  # Adjust the import path as needed

    # Use an invalid URL to force a connection error
    db = DBConnection("test_db", url="mongodb://invalid_url:27017/")
    with pytest.raises(ConnectionError):
        await db.initialize()

    # Ensure the DB is not initialized
    assert not db.is_initialized()

@pytest.mark.asyncio
async def test_count_documents(real_db, db_instance):
    """Test counting documents in a collection."""
    # Initialize the DB
    await db_instance.initialize()

    # Insert test data
    await real_db["test_collection"].insert_many([{"name": "item1"}, {"name": "item2"}])

    # Count all documents
    count = await db_instance.count_documents("test_collection")
    assert count == 2

    # Count documents with a specific query
    count_filtered = await db_instance.count_documents("test_collection", {"name": "item1"})
    assert count_filtered == 1

@pytest.mark.asyncio
async def test_get_document(real_db, db_instance):
    """Test fetching a single document."""
    # Initialize the DB
    await db_instance.initialize()

    # Insert test data
    doc_id = (await real_db["test_collection"].insert_one({"name": "item1"})).inserted_id

    # Fetch the document
    doc = await db_instance.get_document("test_collection", {"_id": doc_id})

    # Assertions
    assert doc is not None
    assert doc["name"] == "item1"

@pytest.mark.asyncio
async def test_get_documents_list(real_db, db_instance):
    """Test fetching a list of documents."""
    # Initialize the DB
    await db_instance.initialize()

    # Insert test data
    await real_db["test_collection"].insert_many([{"name": "item1"}, {"name": "item2"}])

    # Fetch documents
    docs = await db_instance.get_documents_list("test_collection")
    assert len(docs) == 2
    assert docs[0]["name"] == "item1"
    assert docs[1]["name"] == "item2"

@pytest.mark.asyncio
async def test_insert_one(real_db, db_instance):
    """Test inserting a document."""
    # Initialize the DB
    await db_instance.initialize()

    # Insert a document
    doc_id = await db_instance.insert_one("test_collection", {"name": "item1"})
    assert isinstance(doc_id, str)

    # Fetch the inserted document
    doc = await real_db["test_collection"].find_one({"_id": ObjectId(doc_id)})
    assert doc["name"] == "item1"

@pytest.mark.asyncio
async def test_db_close(db_instance):
    """Test closing the database connection."""
    # Initialize the DB
    await db_instance.initialize()

    # Ensure the client is initialized
    assert db_instance.client is not None

    # Close the connection
    db_instance.close()

    # Ensure the client is set to None after closing
    assert db_instance.client is None