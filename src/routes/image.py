from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..utils.image_utils import get_image_abspath
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Define the router
_router = APIRouter(prefix="/image", tags=["Image"])

# Router getter
def get_router():
    """
    Get the FastAPI router for image-related endpoints.

    Returns:
        APIRouter: The configured router.
    """
    return _router

@_router.get("", summary="Get Image", description="Retrieve an image by its filename.")
async def get_image(image: str):
    """
    Retrieve an image by its filename.

    Args:
        image (str): The filename of the image (must end with `.jpg`).

    Returns:
        FileResponse: The image file as a response with media type `image/jpeg`.

    Raises:
        HTTPException (400): If the image filename does not end with `.jpg`.
        HTTPException (404): If the image file is not found.
    """
    logger.info(f"Received request to retrieve image: {image}")

    # Validate image format
    if not image.endswith(".jpg"):
        logger.error(f"Invalid image format for file: {image}")
        raise HTTPException(status_code=400, detail="Invalid Image format. Accepted format: .jpg")
    
    # Get the absolute path of the image
    image_path = get_image_abspath(image)
    logger.debug(f"Resolved image path: {image_path}")
    
    # Raise 404 if the image is not found
    if not image_path:
        logger.error(f"Image not found: {image}")
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Add caching headers to the response
    headers = {
        "Cache-Control": "public, max-age=31536000",
    }
    
    logger.info(f"Serving image: {image}")
    return FileResponse(
        image_path,
        media_type="image/jpeg",
        filename=image,
        headers=headers,
    )