import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.routes.menu import get_router
from src.services import MenuService
from src.models.categories import CategoryModel
from src.models.menuitem import MenuItemModel
from src.services.dependencies import get_menu_service

# Create a FastAPI app and include the router
app = FastAPI()
app.include_router(get_router())

# Create a test client
client = TestClient(app)

@pytest.fixture
def mock_menu_service():
    """Fixture to provide a mock MenuService instance."""
    return AsyncMock(spec=MenuService)

@pytest.fixture
def override_menu_service_dependency(mock_menu_service):
    """Fixture to override the MenuService dependency."""
    app.dependency_overrides[get_menu_service] = lambda: mock_menu_service
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_read_menu_success(mock_menu_service, override_menu_service_dependency):
    """Test successful retrieval of menu statistics."""
    # Mock the service methods
    mock_menu_service.count_items.return_value = 10
    mock_menu_service.count_categories.return_value = 5

    # Make the request
    response = client.get("/menu/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"menu_items": 10, "categories": 5}
    mock_menu_service.count_items.assert_called_once()
    mock_menu_service.count_categories.assert_called_once()

@pytest.mark.asyncio
async def test_read_menu_error(mock_menu_service, override_menu_service_dependency):
    """Test error handling in the read_menu endpoint."""
    # Mock the service to raise an exception
    mock_menu_service.count_items.side_effect = Exception("Database error")

    # Make the request
    response = client.get("/menu/")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}

@pytest.mark.asyncio
async def test_get_categories_success(mock_menu_service, override_menu_service_dependency):
    """Test successful retrieval of categories."""
    # Mock the service method
    mock_menu_service.get_categories.return_value = [
        CategoryModel(id=1, name="Category 1", image_id="image1"),
        CategoryModel(id=2, name="Category 2", image_id="image2"),
    ]

    # Make the request
    response = client.get("/menu/categories")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {"id": 1, "name": "Category 1", "image_id": "image1"},
            {"id": 2, "name": "Category 2", "image_id": "image2"},
        ]
    }
    mock_menu_service.get_categories.assert_called_once()

@pytest.mark.asyncio
async def test_get_categories_error(mock_menu_service, override_menu_service_dependency):
    """Test error handling in the get_categories endpoint."""
    # Mock the service to raise an exception
    mock_menu_service.get_categories.side_effect = Exception("Database error")

    # Make the request
    response = client.get("/menu/categories")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}

@pytest.mark.asyncio
async def test_get_category_items_success(mock_menu_service, override_menu_service_dependency):
    """Test successful retrieval of category items."""
    # Mock the service method
    mock_menu_service.get_category_items.return_value = [
        MenuItemModel(id=1, name="Item 1", category_id=1, price=10.0, image_id="image1"),
        MenuItemModel(id=2, name="Item 2", category_id=1, price=20.0, image_id="image2"),
    ]

    # Make the request
    response = client.get("/menu/categories/1")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {"id": 1, "name": "Item 1", "category_id": 1, "price": 10.0, "image_id": "image1"},
            {"id": 2, "name": "Item 2", "category_id": 1, "price": 20.0, "image_id": "image2"},
        ]
    }
    mock_menu_service.get_category_items.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_get_category_items_error(mock_menu_service, override_menu_service_dependency):
    """Test error handling in the get_category_items endpoint."""
    # Mock the service to raise an exception
    mock_menu_service.get_category_items.side_effect = Exception("Database error")

    # Make the request
    response = client.get("/menu/categories/1")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}

@pytest.mark.asyncio
async def test_get_filtered_items_success(mock_menu_service, override_menu_service_dependency):
    """Test successful retrieval of filtered items."""
    # Mock the service method
    mock_menu_service.get_filtered_items.return_value = [
        MenuItemModel(id=1, name="Item 1", category_id=1, price=10.0, image_id="image1"),
        MenuItemModel(id=2, name="Item 2", category_id=1, price=20.0, image_id="image2"),
    ]

    # Make the request with query parameters
    response = client.get("/menu/item?name=Item")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {"id": 1, "name": "Item 1", "category_id": 1, "price": 10.0, "image_id": "image1"},
            {"id": 2, "name": "Item 2", "category_id": 1, "price": 20.0, "image_id": "image2"},
        ]
    }
    mock_menu_service.get_filtered_items.assert_called_once()

@pytest.mark.asyncio
async def test_get_filtered_items_error(mock_menu_service, override_menu_service_dependency):
    """Test error handling in the get_filtered_items endpoint."""
    # Mock the service to raise an exception
    mock_menu_service.get_filtered_items.side_effect = Exception("Database error")

    # Make the request
    response = client.get("/menu/item?name=Item")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}