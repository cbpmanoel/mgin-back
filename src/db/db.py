import os
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient

class DB:
    def __init__(self, db_name: str, **kwargs):

        if not db_name:
            raise ValueError("Database name is required")
        
        # Get the URL from the kwargs or build it
        url = kwargs.get('url', None)
        if not url:
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 27017)
            
            username = kwargs.get('username', os.getenv('MONGO_USERNAME', None))
            password = kwargs.get('password', os.getenv('MONGO_PASSWORD', None))

            credentials = ""
            if username and password:
                credentials = f'{username}:{password}@'
                
            url = f'mongodb://{credentials}{host}:{port}/'
            
        try:
            self.client = AsyncIOMotorClient(url)
            self.client.admin.command('ping')
            self.db = self.client[db_name]
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")
        
        
    async def count_documents(self, collection_name: str) -> int:
        '''
        Count the number of documents in the collection
        
        Args:
            collection_name (str): Collection Name
            query (dict): Query to filter the documents. Default is {}.
            
        Returns:
            int: Number of documents
        '''
        try:
            collection = self.db[collection_name]
            count = await collection.count_documents()
            return count
        except PyMongoError as e:
            print(f"Database error counting documents in {collection_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error counting documents in {collection_name}: {e}")
            raise
        
        
    async def get_document(self, collection_name: str, query: dict) -> dict:
        '''
        Get a document from the collection
        
        Args:
            collection_name (str): Collection Name
            query (dict): Query to filter the document
            
        Returns:
            dict: Document
        '''
        try:
            collection = self.db[collection_name]
            doc = await collection.find_one(query)
            return doc
        except PyMongoError as e:
            print(f"Database error fetching document from {collection_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error fetching document from {collection_name}: {e}")
            raise
    
    
    async def get_documents_list(self, collection_name: str, query: dict = {}, skip: int = 0, limit: int = 20, sort: list = None) -> list:
        '''
        Get documents from the collection
        
        Args:
            collection_name (str): Collection Name
            query (dict): Query to filter the documents. Default is {}.
            skip (int): Number of documents to skip. Default is 0.
            limit (int): Max length of the list. Default is 20.
            sort (list): List of tuples specifying the field(s) to sort by and the direction. Default is None.
        Returns:
            list: List of documents
        '''
        try:
            collection = self.db[collection_name]
            cursor = collection.find(query)
            
            # Sort the documents if sort is provided
            if sort:
                cursor = cursor.sort(sort)
            
            # Skip and limit the documents 
            cursor = cursor.skip(skip).limit(limit)
            
            docs = await cursor.to_list()
            return docs
        except PyMongoError as e:
            print(f"Database error fetching documents from {collection_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error fetching documents from {collection_name}: {e}")
            raise
        

    async def insert_one(self, collection_name: str, data: dict) -> str:
        '''
        Insert a document into the collection

        Args:
            collection_name (str): Collection Name
            data (dict): Data

        Returns:
            str: Inserted ID
        '''
        try:
            result = await self.db[collection_name].insert_one(data)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Database error inserting document into {collection_name}: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error inserting document into {collection_name}: {e}")
            raise
    
    
    async def close(self) -> None:
        ''' Close the connection '''
        await self.client.close()
