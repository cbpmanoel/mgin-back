from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from .db import DB
from ..models.categories import CategoryModel
from ..models.menuitem import MenuItemModel
from ..models.itemrequestfilter import ItemRequestFilterModel


class MenuService:
    def __init__(self, db: DB):
        self.db = db


    async def get_categories(self) -> List[CategoryModel]:
        """
        Get Categories List
        
        Returns:
            List[CategoryModel]: List of categories
        """
        categories: List[CategoryModel] = []

        try:
            for doc in await self.db.get_documents_list("categories"):
                categories.append(CategoryModel(**doc))
        except ValidationError as e:
            print(f"Validation Error fetching categories: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching categories: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching categories: {e}")
            raise e

        return categories


    async def get_category_items(self, category_id: int) -> List[MenuItemModel]:
        """
        Get Category Items by Category ID

        Args:
            category_id (int): Category ID

        Returns:
            List[MenuItemModel]: List of items in the category
        """
        items: List[MenuItemModel] = []

        try:
            for doc in await self.db.get_documents_list("menu_items", {"category_id": category_id}):
                items.append(MenuItemModel(**doc))
        except ValidationError as e:
            print(f"Validation Error fetching categories: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching categories: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching categories: {e}")
            raise e

        return items


    async def get_filtered_items(
        self, filters: Optional[ItemRequestFilterModel] = None
    ) -> List[MenuItemModel]:
        """
        Get Items with filters

        Args:
            filters (ItemRequestFilterModel): Search Filters

        Returns:
            List[MenuItemModel]: List of items
        """
        query = filters.as_query() if filters else {}
        
        items: List[MenuItemModel] = []

        try:
            for doc in await self.db.get_documents_list("menu_items", query):
                items.append(MenuItemModel(**doc))
        except ValidationError as e:
            print(f"Validation Error fetching categories: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching categories: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching categories: {e}")
            raise e
                
        return items
