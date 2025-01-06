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
- [License](#license)


## Key Features

### **FastAPI Backend**
- **Automatic Documentation**: Interactive API documentation is available at `/docs` and `/redoc`.
- **Data Validation**: Uses **Pydantic** models for request and response validation.
- **Modular Design**: Organized into routes, services, models, and utilities for maintainability.

### **MongoDB Integration**
- Stores menu items, categories, and orders.
- Uses **Motor** for asynchronous database operations.
- Initializes with sample data via [mongo-init.js](mongo-init.js) and [init-data.json](init-data.json).

### **API Functionality**
The API provides the following core functionalities:

#### **Menu Management**
- Retrieve the total number of menu items and categories.
- Fetch a list of all categories or items within a specific category.
- Filter and search for menu items based on customizable criteria.
- Retrieve detailed information about a specific menu item by its ID.

#### **Order Management**
- Create new orders with ease, supporting structured and validated order data.
- Retrieve a list of all orders or fetch a specific order by its ID.

#### **Image Handling**
- Serve static images (e.g., JPG files) dynamically, allowing the kiosk to display product images seamlessly.


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

The following steps will help you set up the application quickly using Docker. The MongoDB database will be populated with sample data located in `resources/init-data.json`.

1. Clone the repository:
    ```sh
    git clone https://github.com/cbpmanoel/mgin-back.git
    cd mgin-kiosk-api
    ```

2. Set up the `.env` file (see [Environment Variables](#environment-variables)).

3. Start the services:
    ```sh
    docker-compose up --build -d
    ```

4. Access the API documentation at `http://localhost:8000/docs` (Swagger).

5. Access the database management at `http://localhost:8081` (Mongo-Express).


## Dependencies

The project requires the following dependencies:

- **Python 3.10+**
- **Docker 24.0+**
- **Docker Compose 1.29+**

Install Python dependencies:
```sh
pip install -r requirements.txt
```


## Installation

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


## Usage

1. Start MongoDB and Mongo-Express:
    ```sh
    docker-compose up mongodb mongo-express -d
    ```

2. Run the FastAPI application:
    ```sh
    python app.py
    ```

3. Access the API documentation at `http://localhost:8000/docs`.


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
# Database settings
MONGO_DB_NAME=test_db          # Name of the MongoDB database
MONGO_HOST=localhost           # MongoDB host address
MONGO_PORT=27017               # MongoDB port
MONGO_USERNAME=root            # MongoDB username
MONGO_PASSWORD=example         # MongoDB password

# API settings
LOG_LEVEL=info                 # Logging level (e.g., info, debug)
UVICORN_LOG_LEVEL=info         # Uvicorn logging level
UVICORN_RELOAD=false           # Enable/disable auto-reload for development

# MongoDB Initialization
MONGO_INITDB_ROOT_USERNAME=root  # Root username for MongoDB initialization
MONGO_INITDB_ROOT_PASSWORD=example  # Root password for MongoDB initialization

# Mongo-Express Settings
ME_CONFIG_MONGODB_ADMINUSERNAME=root  # Admin username for Mongo-Express
ME_CONFIG_MONGODB_ADMINPASSWORD=example  # Admin password for Mongo-Express
ME_CONFIG_BASICAUTH_USERNAME=admin    # Basic auth username for Mongo-Express
ME_CONFIG_BASICAUTH_PASSWORD=password # Basic auth password for Mongo-Express
```

---

## Troubleshooting

- **MongoDB fails to start**:
    - Check logs with `docker-compose logs mongodb`.
- **API fails to start**:
    - Verify the `.env` file is correctly configured.
    - Verify if the FastAPI port is used by another process.
    - If running inside container:
        - Check logs with `docker-compose logs app`.
        - Rerun the container with `docker-compose up --build`.

---

## Contributing

Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).
