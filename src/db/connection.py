import os
import logging
from pymongo.errors import PyMongoError, ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient

# Configure logging
logger = logging.getLogger(__name__)


class DBConnection:
    """
    A class to manage asynchronous MongoDB connections and operations.

    Attributes:
        db_name (str): Name of the database.
        url (str): MongoDB connection URL.
        client (AsyncIOMotorClient): MongoDB client instance.
        db (Database): MongoDB database instance.
        init_successful (bool): Flag to indicate successful initialization.
        socket_timeout (int): Socket timeout in milliseconds.
        connect_timeout (int): Connection timeout in milliseconds.
    """

    def __init__(self, db_name: str, **kwargs):
        """
        Initialize the MongoDB connection.

        Args:
            db_name (str): Name of the database.
            **kwargs: Additional arguments for the MongoDB connection.
                - url (str): Full MongoDB connection URL.
                - host (str): MongoDB host. Default is 'localhost'.
                - port (int): MongoDB port. Default is 27017.
                - username (str): MongoDB username.
                - password (str): MongoDB password.
                - socket_timeout (int): Socket timeout in milliseconds. Default is 5000.
                - connect_timeout (int): Connection timeout in milliseconds. Default is 5000.

        Raises:
            ValueError: If the database name is not provided.
        """
        if not db_name:
            logger.error("Database name is required")
            raise ValueError("Database name is required")

        # Get the URL from the kwargs or build it
        url = kwargs.get('url', None)
        if not url:
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 27017)
            
            username = kwargs.get('username', None)
            password = kwargs.get('password', None)

            credentials = ""
            if username and password:
                credentials = f'{username}:{password}@'
                
            url = f'mongodb://{credentials}{host}:{port}/'
        
        # Get the timeouts
        socket_timeout  = kwargs.get('socket_timeout', 5000)
        connect_timeout = kwargs.get('connect_timeout', 5000)
            
        # Set the attributes
        self.db_name = db_name
        self.url = url
        self.client = None
        self.db = None
        self.init_successful = False
        self.socket_timeout = socket_timeout
        self.connect_timeout = connect_timeout
        
        logger.info(f"Initialized DBConnection for database: {self.db_name}")
        
    def is_initialized(self) -> bool:
        """
        Check if the database connection is initialized.

        Returns:
            bool: True if the database is initialized, False otherwise.
        """
        return self.init_successful
        
    async def initialize(self):
        """
        Asynchronously initialize the MongoDB connection.

        Raises:
            ConnectionError: If the connection to MongoDB fails.
        """
        logger.info(f"Connecting to MongoDB at {self.url}")
        try:
            # Connect to the MongoDB server
            print(f'Connecting to MongoDB at {self.url}')
            self.client = AsyncIOMotorClient(
                self.url,
                connectTimeoutMS=self.connect_timeout,
                socketTimeoutMS=self.socket_timeout
            )
            
            # Test the connection by pinging the admin database
            await self.client.admin.command('ping')
            print('Connected to MongoDB')
            
            # Set the database
            self.db = self.client[self.db_name]
            
            # Set the initialized flag
            self.init_successful = True
            
            logger.info("Successfully connected to MongoDB")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
        except PyMongoError as e:
            logger.error(f"MongoDB error: {e}")
            raise ConnectionError(f"MongoDB error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise ConnectionError(f"Unexpected error: {e}")
        
        
    async def count_documents(self, collection_name: str, query: dict = {}) -> int:
        """
        Count the number of documents in a collection.

        Args:
            collection_name (str): Name of the collection.
            query (dict): Query to filter the documents. Default is {}.

        Returns:
            int: Number of documents matching the query.

        Raises:
            PyMongoError: If a database error occurs.
            Exception: If an unexpected error occurs.
        """
        try:
            collection = self.db[collection_name]
            count = await collection.count_documents(query)
            logger.info(f"Counted {count} documents in collection: {collection_name}")
            return count
        
        except PyMongoError as e:
            logger.error(f"Database error counting documents in {collection_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error counting documents in {collection_name}: {e}")
            raise
        
        
    async def get_document(self, collection_name: str, query: dict) -> dict:
        """
        Retrieve a single document from a collection.

        Args:
            collection_name (str): Name of the collection.
            query (dict): Query to filter the document.

        Returns:
            dict: The document matching the query.

        Raises:
            PyMongoError: If a database error occurs.
            Exception: If an unexpected error occurs.
        """
        try:
            collection = self.db[collection_name]
            doc = await collection.find_one(query)
            logger.info(f"Retrieved document from collection: {collection_name}")
            return doc
        
        except PyMongoError as e:
            logger.error(f"Database error fetching document from {collection_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching document from {collection_name}: {e}")
            raise
    
    
    async def get_documents_list(self, collection_name: str, query: dict = {}, skip: int = 0, limit: int = 20, sort: list = None) -> list:
        """
        Retrieve a list of documents from a collection.

        Args:
            collection_name (str): Name of the collection.
            query (dict): Query to filter the documents. Default is {}.
            skip (int): Number of documents to skip. Default is 0.
            limit (int): Maximum number of documents to return. Default is 20.
            sort (list): List of tuples specifying the field(s) to sort by and the direction. Default is None.

        Returns:
            list: List of documents matching the query.

        Raises:
            PyMongoError: If a database error occurs.
            Exception: If an unexpected error occurs.
        """
        try:
            collection = self.db[collection_name]
            cursor = collection.find(query)
            
            # Sort the documents if sort is provided
            if sort:
                cursor = cursor.sort(sort)
            
            # Skip and limit the documents 
            cursor = cursor.skip(skip).limit(limit)
            
            docs = await cursor.to_list()
            logger.info(f"Retrieved {len(docs)} documents from collection: {collection_name}")
            return docs
        
        except PyMongoError as e:
            logger.error(f"Database error fetching documents from {collection_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching documents from {collection_name}: {e}")
            raise
        

    async def insert_one(self, collection_name: str, data: dict) -> str:
        """
        Insert a single document into a collection.

        Args:
            collection_name (str): Name of the collection.
            data (dict): Document to insert.

        Returns:
            str: The inserted document's ID.

        Raises:
            PyMongoError: If a database error occurs.
            Exception: If an unexpected error occurs.
        """
        try:
            result = await self.db[collection_name].insert_one(data)
            logger.info(f"Inserted document into collection: {collection_name}")
            return str(result.inserted_id)
        
        except PyMongoError as e:
            logger.error(f"Database error inserting document into {collection_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error inserting document into {collection_name}: {e}")
            raise
    
    
    def close(self) -> None:
        """
        Close the MongoDB connection.

        Returns:
            None
        """
        if self.client is not None:
            self.client.close()
            self.client = None
            logger.info("Closed MongoDB connection")