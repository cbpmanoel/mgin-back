from fastapi import Depends
from src.services import MenuService, OrderService
from src.db import DB
from src.db.dependencies import get_db

async def get_menu_service(db: DB = Depends(get_db)) -> MenuService:
    '''
    Get the Menu Service instance
    
    Args:
        db (DB): Database instance
        
    Returns:
        MenuService: Menu Service instance
    '''
    return MenuService(db)

async def get_order_service(db: DB = Depends(get_db)) -> OrderService:
    '''
    Get the Order Service instance
    
    Args:
        db (DB): Database instance
        
    Returns:
        OrderService: Order Service instance
    '''
    return OrderService(db)


