from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from ..db import DB
from ..models.order import OrderModel, StoredOrderModel

class OrderService:
    def __init__(self, db: DB):
        self.db = db
        
        
    async def create_order(self, order: OrderModel) -> str:
        '''
        Create an Order in the database
        
        Args:
            order (OrderModel): Order Object
        
        Returns:
            str: Order ID
        '''
        
        try:
            order_id = await self.db.insert_one("orders", order.model_dump())
            return order_id
        
        except ValidationError as e:
            print(f"Validation Error creating order: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error creating order: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error creating order: {e}")
            raise e
        
        
    async def get_orders(self) -> List[StoredOrderModel]:
        '''
        Get Orders from the database
        
        Returns:
            List[StoredOrderModel]: List of Orders
        '''
        
        try:
            orders: List[StoredOrderModel] = []
            for doc in await self.db.get_documents_list("orders"):
                orders.append(StoredOrderModel(**doc))
            return orders
        
        except ValidationError as e:
            print(f"Validation Error fetching orders: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching orders: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching orders: {e}")
            raise e
        
        
    async def get_order(self, order_id: int) -> Optional[StoredOrderModel]:
        '''
        Get Order by ID
        
        Args:
            order_id (int): Order ID
        
        Returns:
            Optional[StoredOrderModel]: Order Object
        '''
        try:
            doc = await self.db.get_document("orders", {"id": order_id})
            return StoredOrderModel(**doc) if doc else None
        
        except ValidationError as e:
            print(f"Validation Error fetching order: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching order: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching order: {e}")
            raise e