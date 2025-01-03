from .db import DB

async def get_db() -> DB:
    '''
    Get the database instance
    
    Returns:
        DB: Database instance
    '''
    db = DB("kiosk_db", url="mongodb://root:root@localhost:27017")
    return db