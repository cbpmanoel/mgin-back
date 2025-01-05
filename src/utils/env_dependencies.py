import os

def get_db_settings() -> dict:
    '''
    Get the database settings. If in debug mode, return the default settings. Otherwise, get the settings from the environment variables.
    
    Returns:
        dict: The database settings containing the host, port, database name, username, and password.
    
    '''
    if __debug__:
        return {
            'db_name': 'test_db',
            'host': 'localhost',
            'port': 27017,
            'username': 'root',
            'password': 'root'
        }
        
    return {
        'db_name': os.environ.get('MONGO_DB_NAME', 'kiosk_db'),
        'host': os.environ.get('MONGO_HOST', 'localhost'),
        'port': int(os.environ.get('MONGO_PORT', 27017)),
        'username': os.environ.get('MONGO_USERNAME', None),
        'password': os.environ.get('MONGO_PASSWORD', None)
    }