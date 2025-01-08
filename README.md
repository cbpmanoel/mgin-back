# MGin Kiosk API

The **MGin Kiosk API** is a backend application built with **FastAPI** to manage menu items, categories, images, and orders for a kiosk system. It uses **MongoDB** for data storage. The API is designed for ease of use, with automatic documentation, asynchronous request handling, and robust data validation.

## Table of Contents

- [Key Features](#key-features)
  - [FastAPI Backend](#fastapi-backend)
  - [MongoDB Integration](#mongodb-integration)
  - [API Functionality](#api-functionality)
- [Application Structure](#application-structure)
- [Quick Start](#quick-start)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Key Features

### **FastAPI Backend**

- **Automatic Documentation**: Interactive API documentation is available at `/docs` (Swagger) and `/redoc` (ReDoc).
- **Data Validation**: Built with **Pydantic** for validating request and response payloads.
- **Modular Design**: Organized into distinct components like routes, services, models, and utilities for better maintainability.

### **MongoDB Integration**

- Stores data for menu items, categories, and orders.
- Uses **Motor** for seamless asynchronous database operations.
- Initializes sample data using [mongo-init.js](resources/database/mongo-init.js) and [init-data.json](resources/database/init-data.json).

### **API Functionality**

The API supports the following core features:

#### **Menu Management**
- Retrieve the total number of menu items and categories.
- Fetch a list of all categories or specific items within a category.
- Filter and search for menu items based on custom criteria.
- Retrieve detailed information for a specific menu item by its ID.

#### **Order Management**
- Create new orders with structured, validated data.
- Fetch all orders or retrieve a specific order by its ID.

#### **Image Handling**
- Serve static images dynamically for displaying product visuals in the kiosk interface.


## Application Structure

The application is organized into the following key directories and files:

- **`app.py`**: The entry point of the FastAPI application, where the API is initialized and routes are mounted.
- **`src/`**: Contains the core application logic, including:
  - **`routes/`**: Defines the controllers with API endpoints for menu, orders, and images.
  - **`models/`**: Includes Pydantic models for data validation and serialization.
  - **`services/`**: Implements the business logic for handling menu items, orders, and database interactions.
  - **`db/`**: Manages database connections and dependencies.
  - **`utils/`**: Provides utility functions, such as image handling and configuration management.
- **`resources/`**: Contains static resources, including database initialization scripts (`mongo-init.js`, `init-data.json`) and sample images.
- **`tests/`/**: Houses tests for the application.
- **`requirements.txt`**: Lists the dependencies required to run the application.
- **`Dockerfile`**: Defines the Docker image for the FastAPI application.
- **`docker-compose.yml`**: Orchestrates the API, MongoDB, and Mongo-Express services.

## Quick Start

The following steps will help you quickly set up the application using Docker. MongoDB will be automatically initialized with sample data located in `resources/database/init-data.json`.

1. Clone the repository:
    ```sh
    git clone https://github.com/cbpmanoel/mgin-back.git
    cd mgin-back
    ```

2. Set up the `.env` file:
   Refer to the [Environment Variables](#environment-variables) section for required configurations.

3. Start the application with Docker:
    ```sh
    docker-compose up --build -d
    ```

4. Access the FastAPI documentation:
    - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

5. Optional: Access the Mongo-Express interface for managing the database:
    - [http://localhost:8081](http://localhost:8081)


## Dependencies

The project requires the following dependencies:

- **Python 3.10+**
- **Docker 24.0+**
- **Docker Compose 1.29+**

Install Python dependencies:

```sh
pip install -r requirements.txt
```

**The current version has been developed and tested on Ubuntu 20.04 Desktop and Ubuntu 22.04 (WSL2).**

## Installation

1. (Optional) Install [pyenv](https://github.com/pyenv/pyenv-installer) for Python version management.

1. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up the `.env` file (see [Environment Variables](#environment-variables)).


#### (Optional) MongoDB Local Installation and Initialization

If you prefer to run MongoDB locally instead of using Docker, you can install it via the official MongoDB repository:

1. Use the provided [`mongodb_install_local.sh`](mongodb_install_local.sh) script:
   ```bash
   chmod +x mongodb_install_local.sh
   sudo ./mongodb_install_local.sh
   ```

   This installs MongoDB with the default root username `root` and password `root`. For more options, run:
   ```bash
   ./mongodb_install_local.sh --help
   ```

2. Install the required Python dependencies for MongoDB populate database script:
   ```bash
   pip install pymongo python-dotenv
   ```

3. Run the [`mongodb_populate.py`](mongodb_populate.py) script:
   ```bash
   python mongodb_populate.py
   ```

   - **Default Behavior**: If no file is specified, the script uses `resources/database/init-data.json` to populate the database.
   - Default MongoDB connection settings:
     - **Host**: `localhost`
     - **Port**: `27017`
     - **Database**: `test_db`
     - **Username**: `root`
     - **Password**: `example`

3. For more options, run:
   ```bash
   python mongodb_populate.py --help
   ```

4. Verify the populated database using the MongoDB shell (`mongosh`) or a GUI tool like MongoDB Compass.

#### Notes:
- The default [`init-data.json`](resources/database/init-data.json) file contains sample data for menu items and categories. If no custom file is specified, this data will be used.
- The `.env` file must be updated with the correct MongoDB connection settings for the API to work properly. Make sure the values for MongoDB related settings match the database configuration.


## Usage

1. Start MongoDB and Mongo-Express containers, if using Docker:

    ```sh
    docker-compose up mongodb mongo-express -d
    ```

2. Run the FastAPI application:

    ```sh
    python app.py
    ```

3. Access the API documentation at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.

## API Endpoints

### **Menu Endpoints**

- `GET /menu/` - Retrieve the total number of menu items and categories.
- `GET /menu/categories` - Retrieve all categories.
- `GET /menu/categories/{category_id}` - Retrieve items in a specific category.
- `GET /menu/item` - Filter and search for menu items.
- `GET /menu/item/{item_id}` - Retrieve a specific item by ID.

### **Order Endpoints**

- `POST /order/` - Create a new order.
- `GET /order/` - Retrieve all orders.
- `GET /order/{order_id}` - Retrieve a specific order by ID.

### **Image Endpoints**

- `GET /image/{filename}` - Retrieve a JPG image by filename.

## Testing

Run tests:

```sh
pytest tests/
```

Generate a test coverage report:

```sh
pytest tests/ --cov=app
```

## Environment Variables

The following environment variables are required to configure the application. Create a `.env` file in the root directory and populate it with the example below:

```env
# Database settings used by the API
MONGO_DB_NAME=test_db
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USERNAME=root
MONGO_PASSWORD=example

# API settings
LOG_LEVEL=info
UVICORN_LOG_LEVEL=info
UVICORN_RELOAD=false

# MongoDB Initialization
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=example

# Mongo-Express Settings
ME_CONFIG_MONGODB_ADMINUSERNAME=root
ME_CONFIG_MONGODB_ADMINPASSWORD=example
ME_CONFIG_BASICAUTH_USERNAME=admin
ME_CONFIG_BASICAUTH_PASSWORD=password
```

---

## Troubleshooting

- **MongoDB fails to start**:
  - Check logs with `docker-compose logs mongodb`.
- **API fails to start**:
  - Verify the `.env` file is correctly configured.
  - Rebuild the container if the `.env` file changes.
  - Verify if the FastAPI port is used by another process.
  - If running inside a container:
    - Check logs with `docker-compose logs app`.
    - Rerun the container with `docker-compose up --build`.
- **API fails to connect to MongoDB**:
    - Verify the MongoDB connection settings in the `.env` file.
    - Check the MongoDB logs for any errors.
    - Ensure the MongoDB container or service is running.
- **API fails to fetch data from MongoDB**:
    - Verify the MongoDB data is correctly inserted.
    - Verify the MongoDB connection settings in the `.env` file.
    - Check the MongoDB logs for any errors.
    - If running inside a container:
        - Check logs with `docker-compose logs app`.
        - Rerun the container with `docker-compose up --build`.
        - Verify if the MongoDB host address is set to `mongodb`, which is the name of the MongoDB service.

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.
