from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from ..db import DBConnection
from ..models.categories import CategoryModel
from ..models.menuitem import MenuItemModel
from ..models.itemrequestfilter import ItemRequestFilterModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MenuService:
    """
    A service class to handle menu-related operations such as fetching categories, items, and applying filters.

    Attributes:
        db (DBConnection): An instance of the database connection.
    """

    def __init__(self, db: DBConnection):
        """
        Initialize the MenuService with a database connection.

        Args:
            db (DBConnection): An instance of the database connection.
        """
        self.db = db
        logger.info("MenuService initialized with database connection")


    async def get_categories(self) -> List[CategoryModel]:
        """
        Retrieve a list of all categories.

        Returns:
            List[CategoryModel]: A list of `CategoryModel` instances representing the categories.

        Raises:
            ValidationError: If there is an issue validating the data from the database.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        categories: List[CategoryModel] = []

        try:
            logger.info("Fetching all categories")
            for doc in await self.db.get_documents_list("categories"):
                categories.append(CategoryModel(**doc))
                
            logger.info(f"Fetched {len(categories)} categories")
            return categories
        
        except ValidationError as e:
            logger.error(f"Validation Error fetching categories: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error fetching categories: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error fetching categories: {e}")
            raise e


    async def get_category_items(self, category_id: int) -> List[MenuItemModel]:
        """
        Retrieve a list of items belonging to a specific category.

        Args:
            category_id (int): The ID of the category.

        Returns:
            List[MenuItemModel]: A list of `MenuItemModel` instances representing the items in the category.

        Raises:
            ValidationError: If there is an issue validating the data from the database.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        items: List[MenuItemModel] = []

        try:
            logger.info(f"Fetching items for category ID: {category_id}")
            for doc in await self.db.get_documents_list("menu_items", {"category_id": category_id}):
                items.append(MenuItemModel(**doc))
                
            logger.info(f"Fetched {len(items)} items for category ID: {category_id}")
            return items
        
        except ValidationError as e:
            logger.error(f"Validation Error fetching category items: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error fetching category items: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error fetching category items: {e}")
            raise e
        
        
    async def get_item(self, item_id: int) -> Optional[MenuItemModel]:
        """
        Retrieve a specific item by its ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            Optional[MenuItemModel]: An instance of `MenuItemModel` representing the item, or `None` if not found.

        Raises:
            ValidationError: If there is an issue validating the data from the database.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        try:
            logger.info(f"Fetching item with ID: {item_id}")
            doc = await self.db.get_document("menu_items", {"_id": item_id})
            
            if not doc:
                logger.warning(f"Item not found with ID: {item_id}")
                return None
            
            logger.info(f"Fetched item with ID: {item_id}")
            return MenuItemModel(**doc)
        
        except ValidationError as e:
            logger.error(f"Validation Error fetching item: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error fetching item: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error fetching item: {e}")
            raise e


    async def get_filtered_items(
        self, filters: Optional[ItemRequestFilterModel] = None
    ) -> List[MenuItemModel]:
        """
        Retrieve a list of items filtered by specific criteria.

        Args:
            filters (Optional[ItemRequestFilterModel]): An instance of `ItemRequestFilterModel` containing filter criteria. Defaults to `None`.

        Returns:
            List[MenuItemModel]: A list of `MenuItemModel` instances representing the filtered items.

        Raises:
            ValidationError: If there is an issue validating the data from the database.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        query = filters.as_query() if filters else {}
        
        items: List[MenuItemModel] = []

        try:
            logger.info("Fetching filtered items")
            for doc in await self.db.get_documents_list("menu_items", query):
                items.append(MenuItemModel(**doc))
                
            logger.info(f"Fetched {len(items)} filtered items")
            return items
                
        except ValidationError as e:
            logger.error(f"Validation Error fetching filtered items: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error fetching filtered items: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error fetching filtered items: {e}")
            raise e
                
    
    async def count_categories(self) -> int:
        """
        Count the total number of categories.

        Returns:
            int: The total number of categories.

        Raises:
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        try:
            logger.info("Counting categories")
            count = await self.db.count_documents("categories")
            
            logger.info(f"Total categories: {count}")
            return count
        
        except PyMongoError as e:
            logger.error(f"Database error counting categories: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error counting categories: {e}")
            raise

    
    async def count_items(self) -> int:
        """
        Count the total number of items.

        Returns:
            int: The total number of items.

        Raises:
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        try:
            logger.info("Counting items")
            count = await self.db.count_documents("menu_items")
            
            logger.info(f"Total items: {count}")
            return count
        
        except PyMongoError as e:
            logger.error(f"Database error counting items: {e}")
            raise
        
        except Exception as e:
            logger.error(f"Unexpected error counting items: {e}")
            raise