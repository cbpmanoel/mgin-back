from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from ..db import DBConnection
from ..models.order import OrderModel
from bson import ObjectId

class OrderService:
    def __init__(self, db: DBConnection):
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
            # Convert dict to OrderModel
            if isinstance(order, dict):
                order = OrderModel(**order)
            
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
        
        
    async def get_orders(self) -> List[OrderModel]:
        '''
        Get Orders from the database
        
        Returns:
            List[OrderModel]: List of Orders
        '''
        
        try:
            orders: List[OrderModel] = []
            for doc in await self.db.get_documents_list("orders"):
                if doc:  
                    # Convert dict to OrderModel       
                    docToStore = OrderModel(**doc) if isinstance(doc, dict) else doc
                    orders.append(docToStore)
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
        
        
    async def get_order(self, order_id: str) -> Optional[OrderModel]:
        '''
        Get Order by ID
        
        Args:
            order_id (int): Order ID
        
        Returns:
            Optional[OrderModel]: Order Object
        '''
        try:
            doc = await self.db.get_document("orders", {"_id": ObjectId(order_id)})
            return OrderModel(**doc) if doc else None
        
        except ValidationError as e:
            print(f"Validation Error fetching order: {e}")
            raise e
        except PyMongoError as e:
            print(f"Database Error fetching order: {e}")
            raise e
        except Exception as e:
            print(f"Unknown Error fetching order: {e}")
            raise e