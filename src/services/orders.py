from typing import List, Optional
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from ..db import DBConnection
from ..models.order import OrderModel
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class OrderService:
    """
    A service class to handle order-related operations such as creating, retrieving, and managing orders.

    Attributes:
        db (DBConnection): An instance of the database connection.
    """

    def __init__(self, db: DBConnection):
        """
        Initialize the OrderService with a database connection.

        Args:
            db (DBConnection): An instance of the database connection.
        """
        self.db = db
        logger.info("OrderService initialized with database connection")
        
        
    async def create_order(self, order: OrderModel) -> str:
        """
        Create a new order in the database.

        Args:
            order (OrderModel): An instance of `OrderModel` representing the order to be created.

        Returns:
            str: The ID of the newly created order.

        Raises:
            ValidationError: If there is an issue validating the order data.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        try:
            logger.info("Creating a new order")
            
            # Convert dict to OrderModel if necessary
            if isinstance(order, dict):
                order = OrderModel(**order)
            
            # Insert the order into the database
            order_id = await self.db.insert_one("orders", order.model_dump())
            logger.info(f"Order created successfully with ID: {order_id}")
            return order_id
        
        except ValidationError as e:
            logger.error(f"Validation Error creating order: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error creating order: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error creating order: {e}")
            raise e
        
        
    async def get_orders(self) -> List[OrderModel]:
        """
        Retrieve a list of all orders from the database.

        Returns:
            List[OrderModel]: A list of `OrderModel` instances representing the orders.

        Raises:
            ValidationError: If there is an issue validating the order data.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        try:
            logger.info("Fetching all orders")
            orders: List[OrderModel] = []
            
            # Fetch all orders from the database
            for doc in await self.db.get_documents_list("orders"):
                if doc:  
                    # Convert dict to OrderModel if necessary
                    docToStore = OrderModel(**doc) if isinstance(doc, dict) else doc
                    orders.append(docToStore)
                    
            logger.info(f"Fetched {len(orders)} orders")
            return orders
        
        except ValidationError as e:
            logger.error(f"Validation Error fetching orders: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error fetching orders: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error fetching orders: {e}")
            raise e
        
        
    async def get_order(self, order_id: str) -> Optional[OrderModel]:
        """
        Retrieve a specific order by its ID.

        Args:
            order_id (str): The ID of the order to retrieve.

        Returns:
            Optional[OrderModel]: An instance of `OrderModel` representing the order, or `None` if not found.

        Raises:
            ValidationError: If there is an issue validating the order data.
            PyMongoError: If there is a database-related error.
            Exception: If an unexpected error occurs.
        """
        try:
            logger.info(f"Fetching order with ID: {order_id}")
            doc = await self.db.get_document("orders", {"_id": ObjectId(order_id)})
            
            if not doc:
                logger.warning(f"Order not found with ID: {order_id}")
                return None
            
            logger.info(f"Fetched order with ID: {order_id}")
            return OrderModel(**doc)
        
        except ValidationError as e:
            logger.error(f"Validation Error fetching order: {e}")
            raise e
        except PyMongoError as e:
            logger.error(f"Database Error fetching order: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unknown Error fetching order: {e}")
            raise e