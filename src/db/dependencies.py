from .connection import DBConnection
from ..utils.env_dependencies import get_db_settings

async def get_db() -> DBConnection:
    '''
    Get the database instance
    
    Returns:
        DB: Database instance
    '''
    db_settings = get_db_settings()
    
    # Create a new instance of the database
    db_instance = DBConnection(db_settings.db_name,
                     host = db_settings.host,
                     port = db_settings.port,
                     username = db_settings.username,
                     password = db_settings.password)
    
    # Initialize the database
    await db_instance.initialize()
    
    return db_instance