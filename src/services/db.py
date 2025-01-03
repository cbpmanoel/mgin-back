from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient

class DB:
    def __init__(self, host, port, db_name):
        self.client = AsyncIOMotorClient(host, port)
        self.db = self.client[db_name]
        
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
    
    
    async def get_documents_list(self, collection_name: str, query: dict = {}, skip: int = 0, limit: int = 20) -> list:
        '''
        Get documents from the collection
        
        Args:
            collection_name (str): Collection Name
            query (dict): Query to filter the documents. Default is {}.
            skip (int): Number of documents to skip. Default is 0.
            limit (int): Max length of the list. Default is 20.
            
        Returns:
            list: List of documents
        '''
        try:
            collection = self.db[collection_name]
            docs = await collection.find(query).skip(skip).limit(limit).to_list()
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