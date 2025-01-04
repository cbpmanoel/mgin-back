import os, sys
from typing import Optional
from pathlib import Path

def get_image_abspath(image: str) -> Optional[str]:
    '''
    Get the path of an image
    
    Args:
        image (str): Image filename with extension
    
    Returns:
        Optional[str]: Absolute path of the image or None if not found
    '''
    
    if not image:
        return None
    
    images_folder = os.path.join(os.path.abspath(sys.argv[0]), 'resources/images')
    image_path    = Path(os.path.join(images_folder, image))
    
    # Check if the image exists and is a file
    if image_path.exists() and image_path.is_file():
        return image_path
    
    return None
