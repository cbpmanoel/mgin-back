from .db import DB

async def get_db() -> DB:
    '''
    Get the database instance
    
    Returns:
        DB: Database instance
    '''
    # Create a new instance of the database
    db_instance = DB("kiosk_db", url="mongodb://root:root@localhost:27017")
    
    # Initialize the database
    await db_instance.initialize()
    
    return db_instance