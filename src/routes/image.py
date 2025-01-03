from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..services.images import get_image_abspath

# Define the router
_router = APIRouter(prefix="/image", tags=["Image"])

# Router getter
def get_router():
    return _router

# Route: /image
@_router.get("")
async def get_image(image: str):
    '''
    Return the image
    '''
    if not image:
        raise HTTPException(status_code=400, detail="Image ID is required")
    if not image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Invalid Image format. Accepted format: .jpg")
    
    image_path = get_image_abspath(image)
    
    if image_path:
        return FileResponse(image_path, media_type="image/jpeg", filename=image)
    
    raise HTTPException(status_code=404, detail="Image not found")
    