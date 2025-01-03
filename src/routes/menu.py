from fastapi import APIRouter, HTTPException, Query, Depends
from src.models.itemrequestfilter import ItemRequestFilterModel
from src.services.menu import MenuService

# Define the router
_router = APIRouter(prefix="/menu", tags=["Menu"])

# Router getter
def get_router():
    return _router

# Menu Service Session Object
menu_service: MenuService = None
def set_menu_service(service: MenuService):
    global menu_service
    menu_service = service
    
def get_menu_service() -> MenuService:
    return menu_service

# Router routes
@_router.get("/")
async def read_menu():
    ''' Get Menu '''
    return {"menu": "This is the menu"}

@_router.get("/categories")
async def get_categories() -> dict:
    '''
    Get Categories List
    '''
    return {"categories": []}

@_router.get("/categories/{category_id}")
async def get_category_items(category_id: int) -> dict:
    '''
    Get Category Items by Category ID
    '''
    return {"category_id": category_id}

@_router.get("/item")
async def get_filtered_items(model: ItemRequestFilterModel) -> dict:
    '''
    Get Items with filters
    '''
    return {"menu_items": []}
    