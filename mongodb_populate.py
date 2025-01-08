#!python

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    import pymongo
except ImportError:
    print('Missing packages. Please run:')
    print('     pip install pymongo python-dotenv')
    sys.exit(1)
    
from pymongo import MongoClient
    
# Description
DESCRIPTION = '''
This script populates a MongoDB database with initial data, read from a JSON file.
MongoDB connection settings can be passed as command-line arguments, otherwise, the script will use the default values.

Default values:
    - Host: localhost
    - Port: 27017
    - Database: test_db
    - User: root
    - Password: example
'''
    
# Constants
DROP_MSG        = 'Please use the --drop flag to drop the database and re-populate it.'
MONGO_INIT_FILE = '/resources/database/init-data.json'
COLLECTIONS     = ['menu_items', 'categories']

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB   = 'test_db'
MONGO_USER = 'root'
MONGO_PASSWORD = 'example'

# Lambdas for colored output
def red(text: str) -> str: return f'\033[91m{text}\033[0m'
def boldgreen(text: str) -> str: return f'\033[1m\033[92m{text}\033[0m'

# Schemas
@dataclass
class Item:
    category_id: int
    id: int
    image_id: str
    name: str
    price: float
    
    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"Price must be greater than 0")
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self.image_id.strip():
            raise ValueError("Image ID cannot be empty")
        self.name = self.name.strip().title()


@dataclass
class Category:
    id: int
    name: str
    image_id: str
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self.image_id.strip():
            raise ValueError("Image ID cannot be empty")
        self.name = self.name.strip().title()


@dataclass
class DataSchema:
    items: List[Item]
    categories: List[Category]
    
    
# Create the argument parser object
def create_parser():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--file', help='Path to the JSON file containing the initial data')
    parser.add_argument('--host', help='MongoDB host')
    parser.add_argument('--port', help='MongoDB port')
    parser.add_argument('--db',   help='MongoDB database name')
    parser.add_argument('--user', help='MongoDB username')
    parser.add_argument('--pwd',  help='MongoDB password')
    parser.add_argument('--drop', help='Drop the database before populating. ', action='store_true') # Force false by default
    
    return parser


# Load the initial data from the JSON file
def load_init_data(file) -> dict:
    with open(file, 'r') as f:
        data = json.load(f)
    return data


# Validate the data
def validate_init_data(data: dict) -> bool:
    try:
        # Parse items
        items = [Item(**item) for item in data.get("items", [])]
        
        # Parse categories
        categories = [Category(**category) for category in data.get("categories", [])]
        
        # Validate the entire structure
        DataSchema(items=items, categories=categories)
        return True
    
    except (TypeError, ValueError) as e:
        print(f"Data validation failed: {e}")
        return False


# Validate collections against a dictionary of expected counts for each collection
def validate_collections(db: MongoClient, collections: Dict[str, int]) -> bool:
    # Check if the collections exist and if they are empty
    missing_collections = [collection for collection in collections.keys() if collection not in db.list_collection_names()]
    if missing_collections:
        print(f'Database is missing the following collections: {missing_collections}')
        return False
        
    # Check if the collections have the correct number of documents
    empty_collections = [collection for collection in collections.keys() if db[collection].count_documents({}) != collections[collection]]
    if empty_collections:
        print(f'The following collections are empty or have the wrong number of documents: {empty_collections}.')
        for collection in empty_collections:
            print(f'{collection} - Expected: {collections[collection]} documents, found: {db[collection].count_documents({})}.')
        return False
    
    return True
    
    
# Initialize the connection to the MongoDB server
def create_db_connection(db_name: str, host: str, port: int, user: str = None, password: str = None) -> MongoClient:
    # Build the connection URL
    credentials = f'{user}:{password}@' if user and password else ''
    name = f'/{db_name}' if db_name else ''
    url = f'mongodb://{credentials}{host}:{port}{name}'

    try:
        # Connect to the MongoDB server
        client = MongoClient(
                    url,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    serverSelectionTimeoutMS=5000
                )
    
        # Check if the connection is successful
        _result = client.admin.command("ismaster")
        
        # Check if the user has the necessary permissions to create a database
        if not check_permissions_create_db(client):
            exit_with_msg('User does not have the necessary permissions to create a database.', 1)
            
        return client

    except pymongo.errors.ConnectionFailure as e:
        exit_with_msg(f'Error connecting to the MongoDB server: {e}', 1)
        

# Check if the user has the necessary permissions to create a database
def check_permissions_create_db(client: MongoClient):
    try:
        # Connect to the admin database
        db = client.admin

        # Get the current user's information
        current_user = db.command('connectionStatus')['authInfo']['authenticatedUsers'][0]['user']
        user_info = db.command('usersInfo', {'user': current_user, 'db': 'admin'})

        # Check if the user has any of the roles that allow database creation
        allowed_roles = ['root', 'dbAdminAnyDatabase', 'userAdminAnyDatabase']
        user_roles = user_info['users'][0]['roles']
        
        return any(role['role'] in allowed_roles for role in user_roles)
    
    except Exception as e:
        exit_with_msg(f'An error occurred while checking permissions: {e}', 1)


# Exit with a message
def exit_with_msg(msg: str, code: int):
    msg = f'\n{msg}\n'
    print(code and red(msg) or boldgreen(msg))
    sys.exit(code)


# Connect to the MongoDB server
def main(mongo_settings: dict = None, init_file: str = None):
    try:
        db_name = mongo_settings.get('db')
        
        # Load and validate the initial data
        print(boldgreen('\nLoading the initial data...'))
        data = load_init_data(init_file)
        if not validate_init_data(data):
            exit_with_msg('Data file is invalid!', 1)
            
        # Rename the items collection to menu_items
        data['menu_items'] = data.pop('items')
        
        # Connect to the MongoDB server
        print(boldgreen('\nConnecting to the MongoDB server at:'))
        print(f'    Host: {mongo_settings["host"]}')
        print(f'    Port: {mongo_settings["port"]}')
        print(f'    User: {mongo_settings["user"]}')
        
        client = create_db_connection(
            "",
            host=mongo_settings['host'],
            port=int(mongo_settings['port']),
            user=mongo_settings['user'],
            password=mongo_settings['pass']
        )
        
        db = client[db_name]
        
        # Check if the database exists
        if db_name in client.list_database_names():
            print(f'Database {db_name} found.')
            # Whether to drop the database or not
            if not args.drop:
                # Check if the collections exist and if they are empty
                if not validate_collections(db, {collection: len(data[collection]) for collection in COLLECTIONS}):
                    print(red('Database is not populated correctly.'))
                    exit_with_msg(DROP_MSG, 1)
                    
                print('Database is already populated.')
                exit_with_msg(DROP_MSG, 0)
                            
            # Drop the database
            client.drop_database(db_name)
            print('Database dropped successfully!')
            
        # Create and populate the database
        print(boldgreen('\nPopulating the database...'))
        for collection, docs in data.items():
            print(f'Inserting {len(docs)} documents into the {collection} collection...')
            db[collection].insert_many(docs)
            
        # Check if the collections are populated with the correct number of documents
        print (boldgreen('\nChecking if the collections are populated correctly...'))
        if not validate_collections(db, {collection: len(data[collection]) for collection in COLLECTIONS}):
            exit_with_msg('Database was not populated correctly.', 1)
        
        exit_with_msg(f'Database {db_name} populated successfully!', 0)
        
    except Exception as e:
        exit_with_msg(f'An error occurred: {e}', 1)
        
        
        
# Run the script
if __name__ == '__main__':
    print(boldgreen('\n--- MongoDB Populate Script ---'))
    
    # Parse the command-line arguments
    parser = create_parser()
    args = parser.parse_args()

    # Read the MongoDB configuration from arguments or environment variables
    mongo_settings = {
        'host': args.host or MONGO_HOST,
        'port': args.port or MONGO_PORT,
        'db':   args.db   or MONGO_DB,
        'user': args.user or MONGO_USER,
        'pass': args.pwd  or MONGO_PASSWORD
    }

    # Read the path to the JSON file containing the initial data
    init_file = args.file or f'{os.getcwd()}{MONGO_INIT_FILE}'
    
    # Run
    main(mongo_settings, init_file)