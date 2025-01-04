from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from ..db import DBConnection
from ..models.categories import CategoryModel
from ..models.menuitem import MenuItemModel
from ..models.itemrequestfilter import ItemRequestFilterModel


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
            for doc in await self.db.get_documents_list("categories"):
                categories.append(CategoryModel(**doc))
            return categories
        
        except ValidationError as e:
            print(f"Validation Error fetching categories: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching categories: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching categories: {e}")
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
            for doc in await self.db.get_documents_list("menu_items", {"category_id": category_id}):
                items.append(MenuItemModel(**doc))
            return items
        
        except ValidationError as e:
            print(f"Validation Error fetching category items: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching category items: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching category items: {e}")
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
            doc = await self.db.get_document("menu_items", {"_id": item_id})
            if doc:
                return MenuItemModel(**doc)
            return None
        except ValidationError as e:
            print(f"Validation Error fetching item: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching item: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching item: {e}")
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
            for doc in await self.db.get_documents_list("menu_items", query):
                items.append(MenuItemModel(**doc))
            return items
                
        except ValidationError as e:
            print(f"Validation Error fetching filtered items: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching filtered items: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching filtered items: {e}")
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
            count = await self.db.count_documents("categories")
            return count
        except PyMongoError as e:
            print(f"Database error counting categories: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error counting categories: {e}")
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
            count = await self.db.count_documents("menu_items")
            return count
        except PyMongoError as e:
            print(f"Database error counting items: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error counting items: {e}")
            raise