import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

@pytest_asyncio.fixture(scope="function")
async def real_db():
    """Fixture to provide a real MongoDB instance for integration testing."""
    client = AsyncIOMotorClient("mongodb://root:root@localhost:27017")
    db = client["test_db"]
    yield db
    await client.drop_database("test_db")
    
    if client is not None:
        client.close()

@pytest_asyncio.fixture(scope="function")
async def db_instance():
    """Fixture to provide an instance of the DB class."""
    from src.db import DBConnection
    db = DBConnection("test_db", url="mongodb://root:root@localhost:27017")
    yield db
    if db.is_initialized():
        db.close()