from fastapi import APIRouter, HTTPException, Depends
from src.models.itemrequestfilter import ItemRequestFilterModel
from src.services import MenuService
from src.services.dependencies import get_menu_service

# Define the router
_router = APIRouter(prefix="/menu", tags=["Menu"])

# Router getter
def get_router():
    return _router

# Router routes
@_router.get("/")
async def read_menu(service: MenuService = Depends(get_menu_service)) -> dict:
    ''' Get Menu '''
    try:
        items_count = await service.count_items()
        categories_count = await service.count_categories()
        return {"menu_items": items_count, "categories": categories_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/categories")
async def get_categories(service: MenuService = Depends(get_menu_service)) -> dict:
    '''
    Get Categories List
    '''
    try:
        categories = await service.get_categories()
        return {'data': categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@_router.get("/categories/{category_id}")
async def get_category_items(category_id: int, service: MenuService = Depends(get_menu_service)) -> dict:
    '''
    Get Category Items by Category ID
    '''
    try:
        items = await service.get_category_items(category_id)
        return {'data': items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@_router.get("/item")
async def get_filtered_items(model: ItemRequestFilterModel, service: MenuService = Depends(get_menu_service)) -> dict:
    '''
    Get Items with filters
    '''
    try:
        items = await service.get_filtered_items(model)
        return {'data': items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@_router.get("/item/{item_id}")
async def get_item(item_id: int, service: MenuService = Depends(get_menu_service)) -> dict:
    '''
    Get Item by ID
    '''
    try:
        item = await service.get_item(item_id)
        return {'data': item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))