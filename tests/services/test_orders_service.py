import pytest
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from unittest.mock import AsyncMock, patch
from src.services.orders import OrderService
from src.models.order import OrderModel
from bson import ObjectId

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


@pytest.fixture(scope="function")
def mock_db():
    """Fixture to provide a mock DB instance."""
    return AsyncMock()

@pytest.fixture(scope="function")
def order_service(mock_db):
    """Fixture to provide an OrderService instance with a mock DB."""
    return OrderService(mock_db)

@pytest.fixture(scope="function")
async def real_order_service(db_instance):
    """Fixture to provide an OrderService instance with a real DB."""
    await db_instance.initialize()
    return OrderService(db_instance)

@pytest.mark.asyncio
async def test_create_order_success(order_service, mock_db):
    """Test successful creation of an order."""
    # Mock the database response
    mock_db.insert_one.return_value = "order_id_123"

    # Create an order
    order = get_valid_orders(1)[0] 
    modeled_order = OrderModel(**order)

    # Call the method
    order_id = await order_service.create_order(modeled_order)

    # Assertions
    assert order_id == "order_id_123"
    mock_db.insert_one.assert_called_once_with("orders", modeled_order.model_dump())

@pytest.mark.asyncio
async def test_create_order_validation_error(order_service, mock_db):
    """Test validation error when creating an order."""
    # Mock the database to raise a ValidationError
    mock_db.insert_one.side_effect = ValidationError("Validation Error", [])

    # Create an invalid order
    order = {'id': 'invalid', 'total': '-10.0'}

    # Call the method and expect either ValidationError or TypeError
    with pytest.raises((ValidationError, TypeError)) as exc_info:
        await order_service.create_order(order)

    # Assert that the exception is either ValidationError or TypeError
    assert exc_info.type in (ValidationError, TypeError)

@pytest.mark.asyncio
async def test_create_order_database_error(order_service, mock_db):
    """Test database error when creating an order."""
    # Mock the database to raise a PyMongoError
    mock_db.insert_one.side_effect = PyMongoError("Database error")

    # Create a valid order
    order = get_valid_orders(1)[0]
    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await order_service.create_order(order)

@pytest.mark.asyncio
async def test_get_orders_success(order_service, mock_db):
    """Test successful retrieval of orders."""
    # Mock the database response
    valid_orders = get_valid_orders(2)
    
    # Add an ID to each order to simulate the database response
    for order in valid_orders:
        order["_id"] = "abc"
    
    mock_db.get_documents_list.return_value = valid_orders

    # Call the method
    orders = await order_service.get_orders()

    # Assertions
    assert len(orders) == 2
    assert isinstance(orders[0], OrderModel)
    assert orders[0].id == 'abc'
    mock_db.get_documents_list.assert_called_once_with("orders")

@pytest.mark.asyncio
async def test_get_orders_validation_error(order_service, mock_db):
    """Test validation error when fetching orders."""
    # Mock the database response with invalid data
    mock_db.get_documents_list.return_value = [{"_id": "invalid", "items": [], "total": -10.0}]

    # Call the method and expect a ValidationError
    with pytest.raises(ValidationError):
        await order_service.get_orders()

@pytest.mark.asyncio
async def test_get_orders_database_error(order_service, mock_db):
    """Test database error when fetching orders."""
    # Mock the database to raise a PyMongoError
    mock_db.get_documents_list.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await order_service.get_orders()

@pytest.mark.asyncio
async def test_get_order_success(order_service, mock_db):
    """Test successful retrieval of an order by ID."""
    # Mock the database response
    id = ObjectId()
    stored_order = get_valid_orders(1)[0]
    stored_order["_id"] = id
    
    mock_db.get_document.return_value = stored_order

    # Call the method
    order = await order_service.get_order(str(id))

    # Assertions
    assert isinstance(order, OrderModel)
    assert order.id == str(id)
    mock_db.get_document.assert_called_once_with("orders", {"_id": id})

@pytest.mark.asyncio
async def test_get_order_not_found(order_service, mock_db):
    """Test retrieval of a non-existent order."""
    # Mock the database to return None
    mock_db.get_document.return_value = None

    # Call the method
    id = ObjectId()
    order = await order_service.get_order(str(id))

    # Assertions
    assert order is None
    mock_db.get_document.assert_called_once_with("orders", {"_id": id})

@pytest.mark.asyncio
async def test_get_order_validation_error(order_service, mock_db):
    """Test validation error when fetching an order."""
    # Mock the database response with invalid data
    mock_db.get_document.return_value = {"id": "invalid", "items": [], "total": -10.0}

    # Call the method and expect a ValidationError
    with pytest.raises((TypeError, ValidationError)) as exc_info:
        await order_service.get_order(1)
        
    assert exc_info.type in (ValidationError, TypeError)

@pytest.mark.asyncio
async def test_get_order_database_error(order_service, mock_db):
    """Test database error when fetching an order."""
    # Mock the database to raise a PyMongoError
    mock_db.get_document.side_effect = PyMongoError("Database error")

    # Call the method and expect a PyMongoError
    with pytest.raises(PyMongoError):
        await order_service.get_order(str(ObjectId()))

@pytest.mark.asyncio
async def test_create_order_with_real_db(real_order_service, real_db):
    from bson import ObjectId
    """Test creation of an order with a real MongoDB instance."""
    # Create an order
    order = get_valid_orders(1)[0]

    # Call the method
    service = await real_order_service
    order_id = await service.create_order(order)

    # Assertions
    assert isinstance(order_id, str)

    # Verify the order was inserted
    inserted_order = await real_db["orders"].find_one({"_id": ObjectId(order_id)})
    assert inserted_order is not None
    assert inserted_order["_id"] == ObjectId(order_id)

@pytest.mark.asyncio
async def test_get_orders_with_real_db(real_order_service, real_db):
    """Test retrieval of orders with a real MongoDB instance."""
    # Insert test data
    orders = get_valid_orders(2)
    
    await real_db["orders"].insert_many(orders)

    # Call the method
    service = await real_order_service
    orders = await service.get_orders()

    # Assertions
    assert len(orders) == 2
    assert isinstance(orders[0], OrderModel)

@pytest.mark.asyncio
async def test_get_order_with_real_db(real_order_service, real_db):
    """Test retrieval of an order by ID with a real MongoDB instance."""
    # Insert test data
    order = get_valid_orders(1)[0]
    
    service = await real_order_service
    order_id = await service.create_order(order)

    # Call the method
    response_order = await service.get_order(order_id)

    # Assertions
    assert isinstance(response_order, OrderModel)
    assert response_order.id == order_id
