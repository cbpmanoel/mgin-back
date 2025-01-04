from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.order import OrderModel
from ..services.orders import OrderService
from ..services.dependencies import get_order_service

# Define the router
_router = APIRouter(prefix="/order", tags=["Order"])

# Router getter
def get_router():
    return _router

@_router.post("/", summary="Create an Order", description="Create a new order with the provided details.")
async def create_order(order: OrderModel, service: OrderService = Depends(get_order_service)) -> dict:
    """
    Create a new order.

    Args:
        order (OrderModel): The order details to be created.

    Returns:
        dict: A dictionary containing the status and the ID of the created order.

    Raises:
        HTTPException: If an error occurs during order creation.
    """
    try:
        order_id = await service.create_order(order)
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/", summary="Get All Orders", description="Retrieve a list of all orders.")
async def get_orders(service: OrderService = Depends(get_order_service)) -> dict:
    """
    Retrieve a list of all orders.

    Returns:
        dict: A dictionary containing the list of orders.

    Raises:
        HTTPException: If an error occurs while retrieving orders.
    """
    orders: List[OrderModel] = []
    try:
        orders = await service.get_orders()
        return {'data': orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/{order_id}", summary="Get Order by ID", description="Retrieve a specific order by its ID.")
async def get_order(order_id: str, service: OrderService = Depends(get_order_service)) -> dict:
    """
    Retrieve a specific order by its ID.

    Args:
        order_id (str): The ID of the order to retrieve.

    Returns:
        dict: A dictionary containing the order details.

    Raises:
        HTTPException: If an error occurs while retrieving the order.
    """
    try:
        order: OrderModel = await service.get_order(order_id)
        return {'data': order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))