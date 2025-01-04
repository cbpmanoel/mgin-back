import os
from pathlib import Path
from typing import Optional
from src.utils.constants import IMAGES_FOLDER

def get_image_abspath(image: str, base_dir: Optional[str] = None) -> Optional[str]:
    '''
    Get the absolute path of an image file.

    Args:
        image (str): Image filename with extension.
        base_dir (Optional[str]): Base directory for the images folder. If None, the script's directory is used.

    Returns:
        Optional[str]: Absolute path of the image or None if not found.
    '''
    if not image:
        return None
    
    try:
        
        if base_dir is None:
            base_dir = Path(os.getcwd()) / IMAGES_FOLDER
        
        image_path = Path(base_dir) / image
        
        # Check if the image file exists
        if image_path.exists() and image_path.is_file():
            return str(image_path)
        
        return None
    except Exception as e:
        return None