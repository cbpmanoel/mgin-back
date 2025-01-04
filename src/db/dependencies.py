from .connection import DBConnection
from ..utils.env_dependencies import get_db_settings


async def get_db() -> DBConnection:
    """
    Get the database instance

    Returns:
        DB: Database instance
    """
    db_settings = get_db_settings()

    # Create a new instance of the database
    db_instance = DBConnection(
        db_name=db_settings.get("db_name"),
        host=db_settings.get("host", "localhost"),
        port=db_settings.get("port", 27017),
        username=db_settings.get("username", None),
        password=db_settings.get("password", None),
    )

    # Initialize the database
    await db_instance.initialize()

    return db_instance
