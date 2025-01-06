import pytest
from fastapi import FastAPI, Response, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from unittest.mock import patch
from src.routes.image import get_router

# Create a FastAPI app and include the router
app = FastAPI()
app.include_router(get_router())

# Configure the exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ''' Handle validation errors as bad requests '''    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Invalid request data', 'errors': exc.errors(), 'body': exc.body},
    )


# Create a test client
client = TestClient(app)

@pytest.fixture
def mock_image_file(tmpdir):
    """Fixture to create a mock image file."""
    image_file = tmpdir.join("test_image.jpg")
    image_file.write("dummy content")
    return image_file

@pytest.fixture
def mock_image_utils():
    """Fixture to mock the get_image_abspath function."""
    with patch("src.routes.image.get_image_abspath") as mock:
        yield mock

@pytest.mark.asyncio
async def test_get_image_success(mock_image_file, mock_image_utils):
    """Test successful retrieval of an image."""
    # Mock the get_image_abspath function
    mock_image_utils.return_value = str(mock_image_file)

    # Make the request
    response = client.get("/image/test_image.jpg")

    # Assertions
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.headers["content-disposition"] == 'attachment; filename="test_image.jpg"'
    mock_image_utils.assert_called_once_with("test_image.jpg")

@pytest.mark.asyncio
async def test_get_image_missing_image_id():
    """Test retrieval with a missing image ID."""
    # Make the request without the image parameter
    response = client.get("/image")

    # Assertions
    assert response.status_code == 400
    assert response.json()['detail'] == "Invalid request data"

@pytest.mark.asyncio
async def test_get_image_invalid_format():
    """Test retrieval with an invalid image format."""
    # Make the request with an invalid image format
    response = client.get("/image/test_image.png")

    # Assertions
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid Image format. Accepted format: .jpg"}

@pytest.mark.asyncio
async def test_get_image_not_found(mock_image_utils):
    """Test retrieval of a non-existent image."""
    # Mock the get_image_abspath function to return None
    mock_image_utils.return_value = None

    # Make the request
    response = client.get("/image/non_existent_image.jpg")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "Image not found"}