from dotenv import load_dotenv, find_dotenv
import os, sys
import logging

if __debug__:
    print("Loading environment variables from .env file")
    if not load_dotenv(find_dotenv()):
        print("Failed to load .env file")
        
# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level = LOG_LEVEL,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Uvicorn settings
UVICORN_HOST = os.getenv('UVICORN_HOST', '0.0.0.0')
UVICORN_PORT = int(os.getenv('UVICORN_PORT', 8000))
UVICORN_LOG_LEVEL = os.getenv('UVICORN_LOG_LEVEL', 'info').lower()
UVICORN_RELOAD = os.getenv('UVICORN_RELOAD', 'false').lower() == 'true'

# MongoDB settings
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'test_db')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
MONGO_USERNAME = os.getenv('MONGO_USERNAME', None)
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', None)


def get_db_settings() -> dict:
    '''
    Get the database settings. The settings are read from the environment variables.
    
    Returns:
        dict: The database settings containing the host, port, database name, username, and password.
    
    '''
    return {
        'db_name': MONGO_DB_NAME,
        'host': MONGO_HOST,
        'port': MONGO_PORT,
        'username': MONGO_USERNAME,
        'password': MONGO_PASSWORD
    }