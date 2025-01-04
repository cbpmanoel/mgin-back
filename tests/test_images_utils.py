import os
import pytest
from pathlib import Path
from src.utils.image_utils import get_image_abspath

# Helper function to create a temporary directory and image file
def create_temp_image(tmp_path, filename):
    image_path = tmp_path / filename
    image_path.write_text("dummy image content")
    
    return str(image_path)

# Test cases
def test_valid_image(tmp_path):
    """
    Test that the function returns the correct absolute path for a valid image file.
    """
    # Create a temporary image file
    image_filename = "test_image.jpg"
    image_path = create_temp_image(tmp_path, image_filename)
    
    # Call the function
    result = get_image_abspath(image_filename, base_dir=str(tmp_path))
    
    # Assert the result
    assert result == image_path

def test_invalid_image(tmp_path):
    """
    Test that the function returns None for an invalid image file.
    """
    # Call the function with a non-existent image
    result = get_image_abspath("non_existent_image.jpg", base_dir=str(tmp_path))
    
    # Assert the result
    assert result is None

def test_empty_input():
    """
    Test that the function returns None for empty or invalid input.
    """
    # Call the function with empty input
    result = get_image_abspath("")
    
    # Assert the result
    assert result is None

def test_file_system_error(tmp_path, monkeypatch):
    """
    Test that the function handles file system errors gracefully.
    """
    # Simulate a file system error by mocking os.path.exists to raise an exception
    def mock_exists(*args, **kwargs):
        raise PermissionError("Permission denied")
    
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    # Call the function
    result = get_image_abspath("test_image.jpg", base_dir=str(tmp_path))
    
    # Assert the result
    assert result is None

def test_custom_base_directory(tmp_path):
    """
    Test that the function works with a custom base directory.
    """
    # Create a temporary image file in a custom directory
    custom_dir = tmp_path / "custom_dir"
    custom_dir.mkdir()
    image_filename = "test_image.jpg"
    image_path = create_temp_image(custom_dir, image_filename)
    
    # Call the function with the custom base directory
    result = get_image_abspath(image_filename, base_dir=str(custom_dir))
    
    # Assert the result
    assert result == image_path

def test_default_base_directory(tmp_path, monkeypatch):
    """
    Test that the function uses the script's directory as the default base directory.
    """
    # Create a temporary image file in the default directory
    image_filename = "test_image.jpg"
    image_path = create_temp_image(tmp_path, image_filename)
    
    # Mock the current working directory to be the temporary directory
    monkeypatch.setattr("os.getcwd", lambda: str(tmp_path))
    
    # Call the function without specifying a base directory
    result = get_image_abspath(image_filename)
    
    # Assert the result
    assert result == str(image_path)