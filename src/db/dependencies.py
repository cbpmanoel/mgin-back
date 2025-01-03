from .db import DB

async def get_db() -> DB:
    '''
    Get the database instance
    
    Returns:
        DB: Database instance
    '''
    db = DB("localhost", 27017, "mgin-kiosk")
    return db