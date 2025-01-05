import pytest
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from unittest.mock import AsyncMock, patch
from src.services.menu import MenuService
from src.models.categories import CategoryModel
from src.models.menuitem import MenuItemModel
from src.models.itemrequestfilter import ItemRequestFilterModel

@pytest.fixture(scope="function")
def mock_db():
    """Fixture to provide a mock DB instance."""
    return AsyncMock()

@pytest.fixture(scope="function")
def menu_service(mock_db):
    """Fixture to provide a MenuService instance with a mock DB."""
    return MenuService(mock_db)

@pytest.fixture(scope="function")
async def real_menu_service(db_instance):
    """Fixture to provide a MenuService instance with a real DB."""
    await db_instance.initialize()
    return MenuService(db_instance)

@pytest.mark.asyncio
async def test_get_categories_success(menu_service, mock_db):
    """Test successful retrieval of categories."""
    # Mock the database response
    mock_db.get_documents_list.return_value = [
        {"id": 1, "name": "Category 1", "image_id": "image1"},
        {"id": 2, "name": "Category 2", "image_id": "image2"},
    ]

    # Call the method
    categories = await menu_service.get_categories()

    # Assertions
    assert len(categories) == 2
    assert isinstance(categories[0], CategoryModel)
    assert categories[0].name == "Category 1"
    mock_db.get_documents_list.assert_called_once_with("categories")

@pytest.mark.asyncio
async def test_get_categories_validation_error(menu_service, mock_db):
    """Test validation error when fetching categories."""
    # Mock the database response with invalid data
    mock_db.get_documents_list.return_value = [{"id": "invalid", "name": 123}]

    # Call the method and expect a ValidationError
    with pytest.raises(ValidationError):
        await menu_service.get_categories()

@pytest.mark.asyncio
async def test_get_categories_database_error(menu_service, mock_db):
    """Test database error when fetching categories."""
    # Mock the database to raise a PyMongoError
    mock_db.get_documents_list.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await menu_service.get_categories()

@pytest.mark.asyncio
async def test_get_category_items_success(menu_service, mock_db):
    """Test successful retrieval of items in a category."""
    # Mock the database response
    mock_db.get_documents_list.return_value = [
        {"id": 1, "name": "Item 1", "category_id": 1, "price": 10.0, "image_id": "image1"},
        {"id": 2, "name": "Item 2", "category_id": 1, "price": 20.0, "image_id": "image2"},
    ]

    # Call the method
    items = await menu_service.get_category_items(1)

    # Assertions
    assert len(items) == 2
    assert isinstance(items[0], MenuItemModel)
    assert items[0].name == "Item 1"
    mock_db.get_documents_list.assert_called_once_with("menu_items", {"category_id": 1})

@pytest.mark.asyncio
async def test_get_category_items_validation_error(menu_service, mock_db):
    """Test validation error when fetching category items."""
    # Mock the database response with invalid data
    mock_db.get_documents_list.return_value = [{"id": "invalid", "name": 123, "category_id": 1}]

    # Call the method and expect a ValidationError
    with pytest.raises(ValidationError):
        await menu_service.get_category_items(1)

@pytest.mark.asyncio
async def test_get_category_items_database_error(menu_service, mock_db):
    """Test database error when fetching category items."""
    # Mock the database to raise a PyMongoError
    mock_db.get_documents_list.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await menu_service.get_category_items(1)

@pytest.mark.asyncio
async def test_get_filtered_items_success(menu_service, mock_db):
    """Test successful retrieval of filtered items."""
    # Mock the database response
    mock_db.get_documents_list.return_value = [
        {"id": 1, "name": "Item 1", "category_id": 1, "price": 10.0, "image_id": "image1"},
        {"id": 2, "name": "Item 2", "category_id": 1, "price": 20.0, "image_id": "image2"},
    ]

    # Create a filter
    filters = ItemRequestFilterModel(name="Item 1")

    # Call the method
    items = await menu_service.get_filtered_items(filters)

    # Assertions
    assert len(items) == 2
    assert isinstance(items[0], MenuItemModel)
    assert items[0].name == "Item 1"
    mock_db.get_documents_list.assert_called_once_with("menu_items", filters.as_query())

@pytest.mark.asyncio
async def test_get_filtered_items_no_filters(menu_service, mock_db):
    """Test retrieval of items without filters."""
    # Mock the database response
    mock_db.get_documents_list.return_value = [
        {"id": 1, "name": "Item 1", "category_id": 1, "price": 10.0, "image_id": "image1"},
        {"id": 2, "name": "Item 2", "category_id": 1, "price": 20.0, "image_id": "image2"},
    ]

    # Call the method without filters
    items = await menu_service.get_filtered_items()

    # Assertions
    assert len(items) == 2
    assert isinstance(items[0], MenuItemModel)
    assert items[0].name == "Item 1"
    mock_db.get_documents_list.assert_called_once_with("menu_items", {})

@pytest.mark.asyncio
async def test_get_filtered_items_validation_error(menu_service, mock_db):
    """Test validation error when fetching filtered items."""
    # Mock the database response with invalid data
    mock_db.get_documents_list.return_value = [{"id": "invalid", "name": 123, "category_id": 1}]

    # Call the method and expect a ValidationError
    with pytest.raises(ValidationError):
        await menu_service.get_filtered_items()

@pytest.mark.asyncio
async def test_get_filtered_items_database_error(menu_service, mock_db):
    """Test database error when fetching filtered items."""
    # Mock the database to raise a PyMongoError
    mock_db.get_documents_list.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await menu_service.get_filtered_items()

@pytest.mark.asyncio
async def test_count_categories_success(menu_service, mock_db):
    """Test successful counting of categories."""
    # Mock the database response
    mock_db.count_documents.return_value = 5

    # Call the method
    count = await menu_service.count_categories()

    # Assertions
    assert count == 5
    mock_db.count_documents.assert_called_once_with("categories")

@pytest.mark.asyncio
async def test_count_categories_database_error(menu_service, mock_db):
    """Test database error when counting categories."""
    # Mock the database to raise a PyMongoError
    mock_db.count_documents.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await menu_service.count_categories()

@pytest.mark.asyncio
async def test_count_items_success(menu_service, mock_db):
    """Test successful counting of items."""
    # Mock the database response
    mock_db.count_documents.return_value = 10

    # Call the method
    count = await menu_service.count_items()

    # Assertions
    assert count == 10
    mock_db.count_documents.assert_called_once_with("menu_items")

@pytest.mark.asyncio
async def test_count_items_database_error(menu_service, mock_db):
    """Test database error when counting items."""
    # Mock the database to raise a PyMongoError
    mock_db.count_documents.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await menu_service.count_items()

@pytest.mark.asyncio
async def test_get_categories_with_real_db(real_menu_service, real_db):
    """Test retrieval of categories with a real MongoDB instance."""
    # Insert test data
    await real_db["categories"].insert_many([
        {"id": 1, "name": "Category 1", "image_id": "image1"},
        {"id": 2, "name": "Category 2", "image_id": "image2"},
    ])

    # Call the method
    instance = await real_menu_service
    categories = await instance.get_categories()

    # Assertions
    assert len(categories) == 2
    assert isinstance(categories[0], CategoryModel)
    assert categories[0].name == "Category 1"

@pytest.mark.asyncio
async def test_get_category_items_with_real_db(real_menu_service, real_db):
    """Test retrieval of category items with a real MongoDB instance."""
    # Insert test data
    await real_db["menu_items"].insert_many([
        {"id": 1, "name": "Item 1", "category_id": 1, "price": 10.0, "image_id": "image1"},
        {"id": 2, "name": "Item 2", "category_id": 1, "price": 20.0, "image_id": "image2"},
    ])

    # Call the method
    instance = await real_menu_service
    items = await instance.get_category_items(1)

    # Assertions
    assert len(items) == 2
    assert isinstance(items[0], MenuItemModel)
    assert items[0].name == "Item 1"