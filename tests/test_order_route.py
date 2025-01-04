import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from src.routes.orders import get_router
from src.services.orders import OrderService
from src.models.order import OrderModel
from src.services.dependencies import get_order_service

def get_valid_orders(size: int = 3):
    """Return a list of valid orders in JSON-compatible format."""
    return [
        {
            "total": 20.0,
            "items": [
                {
                    "item": {
                        "category_id": i,
                        "id": i,
                        "name": f"Item {i}",
                        "price": 10.0,
                        "image_id": f"item{i}.jpg",
                    },
                    "quantity": i,
                    "price_at_order": 0.5,
                }
            ],
            "payment": {"type": "card", "amount": 20.0},
            "created_at": "2021-01-01T00:00:00",
        }
        for i in range(1, size + 1)
    ]

# Create a FastAPI app and include the router
app = FastAPI()
app.include_router(get_router())

# Create a test client
client = TestClient(app)

@pytest.fixture
def mock_order_service():
    """Fixture to provide a mock OrderService instance."""
    return AsyncMock(spec=OrderService)

@pytest.fixture
def override_order_service_dependency(mock_order_service):
    """Fixture to override the OrderService dependency."""
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_order_success(mock_order_service, override_order_service_dependency):
    """Test successful creation of an order."""
    # Mock the service method
    mock_order_service.create_order.return_value = "order_id_123"

    # Create an order payload
    order_payload = get_valid_orders(1)[0]

    # Make the request
    response = client.post("/order/", json=order_payload)

    # Assertions
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json().get("order_id") == "order_id_123"
    mock_order_service.create_order.assert_called_once_with(OrderModel(**order_payload))

@pytest.mark.asyncio
async def test_create_order_error(mock_order_service, override_order_service_dependency):
    """Test error handling in the create_order endpoint."""
    # Mock the service to raise an exception
    mock_order_service.create_order.side_effect = Exception("Database error")

    # Create an order payload
    order_payload = get_valid_orders(1)[0]

    # Make the request
    response = client.post("/order/", json=order_payload)

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}

@pytest.mark.asyncio
async def test_get_orders_success(mock_order_service, override_order_service_dependency):
    """Test successful retrieval of orders."""
    # Mock the service method
    
    orders = get_valid_orders(2)
    for i, order in enumerate(orders):
        order["_id"] = f"order_id_12{i}"
    
    mock_order_service.get_orders.return_value = orders

    # Make the request
    response = client.get("/order/")

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"data": orders}
    mock_order_service.get_orders.assert_called_once()

@pytest.mark.asyncio
async def test_get_orders_error(mock_order_service, override_order_service_dependency):
    """Test error handling in the get_orders endpoint."""
    # Mock the service to raise an exception
    mock_order_service.get_orders.side_effect = Exception("Database error")

    # Make the request
    response = client.get("/order/")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}

@pytest.mark.asyncio
async def test_get_order_by_id_success(mock_order_service, override_order_service_dependency):
    """Test successful retrieval of an order by ID."""
    # Mock the service method
    order = get_valid_orders(1)[0]
    order["_id"] = "order_id_123"
    mock_order_service.get_order.return_value = order

    # Make the request
    response = client.get("/order/order_id_123")

    # Assertions
    assert response.status_code == 200
    assert response.json().get('data') == order
    mock_order_service.get_order.assert_called_once_with("order_id_123")

@pytest.mark.asyncio
async def test_get_order_by_id_error(mock_order_service, override_order_service_dependency):
    """Test error handling in the get_order_by_id endpoint."""
    # Mock the service to raise an exception
    mock_order_service.get_order.side_effect = Exception("Database error")

    # Make the request
    response = client.get("/order/order_id_123")

    # Assertions
    assert response.status_code == 500
    assert response.json() == {"detail": "Database error"}