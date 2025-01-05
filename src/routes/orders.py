from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.order import OrderModel
from ..services.orders import OrderService
from ..services.dependencies import get_order_service
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Define the router
_router = APIRouter(prefix="/order", tags=["Order"])

# Router getter
def get_router():
    """
    Get the FastAPI router for order-related endpoints.

    Returns:
        APIRouter: The configured router.
    """
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
        logger.info("Creating a new order")
        order_id = await service.create_order(order)
        
        logger.info(f"Order created successfully with ID: {order_id}")
        return {"status": "success", "order_id": order_id}
    
    except Exception as e:
        logger.error(f"Error creating order: {e}")
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
    try:
        logger.info("Fetching all orders")
        orders = await service.get_orders()
        
        logger.info(f"Fetched {len(orders)} orders")
        return {'data': orders}
    
    except Exception as e:
        logger.error(f"Error fetching orders: {e}")
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
        logger.info(f"Fetching order with ID: {order_id}")
        order = await service.get_order(order_id)
        
        if order:
            logger.info(f"Fetched order with ID: {order_id}")
            return {'data': order}
        else:
            logger.warning(f"Order not found with ID: {order_id}")
            raise HTTPException(status_code=404, detail="Order not found")
        
    except Exception as e:
        logger.error(f"Error fetching order with ID {order_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))