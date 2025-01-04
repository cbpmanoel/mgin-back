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
@_router.get("/", summary="Get Menu Statistics", description="Retrieve the total number of menu items and categories.")
async def read_menu(service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve the total number of menu items and categories.

    Returns:
        dict: A dictionary containing the count of menu items and categories.
    """
    try:
        items_count = await service.count_items()
        categories_count = await service.count_categories()
        return {"menu_items": items_count, "categories": categories_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/categories", summary="Get Categories List", description="Retrieve a list of all categories.")
async def get_categories(service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve a list of all categories.

    Returns:
        dict: A dictionary containing the list of categories.
    """
    try:
        categories = await service.get_categories()
        return {'data': categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/categories/{category_id}", summary="Get Items by Category", description="Retrieve all items belonging to a specific category.")
async def get_category_items(category_id: int, service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve all items belonging to a specific category.

    Args:
        category_id (int): The ID of the category.

    Returns:
        dict: A dictionary containing the list of items in the specified category.
    """
    try:
        items = await service.get_category_items(category_id)
        return {'data': items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/item", summary="Get Filtered Items", description="Retrieve items based on filters.")
async def get_filtered_items(model: ItemRequestFilterModel = Depends(), service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve items based on filters.

    Args:
        model (ItemRequestFilterModel): The filter model containing query parameters.

    Returns:
        dict: A dictionary containing the list of filtered items.
    """
    try:
        items = await service.get_filtered_items(model)
        return {'data': items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/item/{item_id}", summary="Get Item by ID", description="Retrieve a specific item by its ID.")
async def get_item(item_id: int, service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve a specific item by its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: A dictionary containing the item details.
    """
    try:
        item = await service.get_item(item_id)
        return {'data': item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))