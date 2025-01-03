from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.order import OrderModel, StoredOrderModel
from ..services.orders import OrderService
from ..services.dependencies import get_order_service

# Define the router
_router = APIRouter(prefix="/order", tags=["Order"])

# Router getter
def get_router():
    return _router

@_router.post("/")
async def create_order(order: OrderModel, service: OrderService = Depends(get_order_service)) -> dict:
    '''
    Create an Order
    '''
    
    try:
        order_id = await service.create_order(order)
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@_router.get("/")
async def get_orders(service: OrderService = Depends(get_order_service)) -> dict:
    '''
    Get Orders
    '''
    orders: List[StoredOrderModel] = []
    try:
        orders = await service.get_orders()
        return {'data': orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@_router.get("/{order_id}")
async def get_order(order_id: str, service: OrderService = Depends(get_order_service)) -> dict:
    '''
    Get Order by ID
    
    Args:
    order_id (str): Order ID
    '''
    try:
        order: StoredOrderModel = await service.get_order(order_id)
        return {'data': order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
