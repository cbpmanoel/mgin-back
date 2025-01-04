from fastapi import APIRouter, HTTPException, Depends
from src.models.itemrequestfilter import ItemRequestFilterModel
from src.services import MenuService
from src.services.dependencies import get_menu_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define the router
_router = APIRouter(prefix="/menu", tags=["Menu"])

# Router getter
def get_router():
    """
    Get the FastAPI router for menu-related endpoints.

    Returns:
        APIRouter: The configured router.
    """
    return _router

# Router routes
@_router.get("/", summary="Get Menu Statistics", description="Retrieve the total number of menu items and categories.")
async def read_menu(service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve the total number of menu items and categories.

    Returns:
        dict: A dictionary containing the count of menu items and categories.

    Raises:
        HTTPException (500): If an unexpected error occurs.
    """
    try:
        logger.info("Fetching menu statistics")
        items_count = await service.count_items()
        categories_count = await service.count_categories()
        
        logger.info(f"Menu statistics fetched: {items_count} items, {categories_count} categories")
        return {"menu_items": items_count, "categories": categories_count}
    
    except Exception as e:
        logger.error(f"Error fetching menu statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/categories", summary="Get Categories List", description="Retrieve a list of all categories.")
async def get_categories(service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve a list of all categories.

    Returns:
        dict: A dictionary containing the list of categories.

    Raises:
        HTTPException (500): If an unexpected error occurs.
    """
    try:
        logger.info("Fetching categories list")
        categories = await service.get_categories()
        
        logger.info(f"Fetched {len(categories)} categories")
        return {'data': categories}
    
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/categories/{category_id}", summary="Get Items by Category", description="Retrieve all items belonging to a specific category.")
async def get_category_items(category_id: int, service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve all items belonging to a specific category.

    Args:
        category_id (int): The ID of the category.

    Returns:
        dict: A dictionary containing the list of items in the specified category.

    Raises:
        HTTPException (500): If an unexpected error occurs.
    """
    try:
        logger.info(f"Fetching items for category ID: {category_id}")
        items = await service.get_category_items(category_id)
        
        logger.info(f"Fetched {len(items)} items for category ID: {category_id}")
        return {'data': items}
    
    except Exception as e:
        logger.error(f"Error fetching items for category ID {category_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/item", summary="Get Filtered Items", description="Retrieve items based on filters.")
async def get_filtered_items(model: ItemRequestFilterModel = Depends(), service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve items based on filters.

    Args:
        model (ItemRequestFilterModel): The filter model containing query parameters.

    Returns:
        dict: A dictionary containing the list of filtered items.

    Raises:
        HTTPException (500): If an unexpected error occurs.
    """
    try:
        logger.info("Fetching filtered items")
        items = await service.get_filtered_items(model)
        
        logger.info(f"Fetched {len(items)} filtered items")
        return {'data': items}
    
    except Exception as e:
        logger.error(f"Error fetching filtered items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@_router.get("/item/{item_id}", summary="Get Item by ID", description="Retrieve a specific item by its ID.")
async def get_item(item_id: int, service: MenuService = Depends(get_menu_service)) -> dict:
    """
    Retrieve a specific item by its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: A dictionary containing the item details.

    Raises:
        HTTPException (500): If an unexpected error occurs.
    """
    try:
        logger.info(f"Fetching item with ID: {item_id}")
        item = await service.get_item(item_id)
        
        if item:
            logger.info(f"Fetched item with ID: {item_id}")
            return {'data': item}
        else:
            logger.warning(f"Item not found with ID: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
        
    except Exception as e:
        logger.error(f"Error fetching item with ID {item_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    