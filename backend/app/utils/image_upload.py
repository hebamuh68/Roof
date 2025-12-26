from fastapi import UploadFile, HTTPException, status
from pathlib import Path
import shutil
import uuid
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Get upload directory - should match the static files mount in main.py
# Default to backend/static/images for consistency with static file serving
BACKEND_DIR = Path(__file__).parent.parent.parent  # backend/
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", str(BACKEND_DIR / "static" / "images")))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed image MIME types
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


def get_unique_filename(filename: str) -> str:
    """Generate a unique filename using UUID while preserving extension."""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return f"{uuid.uuid4().hex}{ext}"


def validate_image_file(file: UploadFile) -> None:
    """Validate that the uploaded file is a valid image."""
    # Check content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image type. Allowed: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    
    # Check filename extension
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )


async def save_image_file(file: UploadFile) -> str:
    """
    Save an uploaded image file to the filesystem and return the filename.
    
    Args:
        file: The uploaded file
        
    Returns:
        The unique filename of the saved file
    """
    # Validate the file
    validate_image_file(file)
    
    # Reset file pointer to beginning (in case it was already read)
    await file.seek(0)
    
    # Generate unique filename
    unique_filename = get_unique_filename(file.filename)
    file_path = UPLOAD_DIR / unique_filename
    
    # Check file size (read in chunks to avoid loading entire file into memory)
    file_size = 0
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(8192)  # Read in 8KB chunks
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                # Delete the partially written file
                file_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024):.1f}MB"
                )
            buffer.write(chunk)
    
    return unique_filename


async def save_multiple_images(files: List[UploadFile]) -> List[str]:
    """
    Save multiple image files and return their filenames.
    
    Args:
        files: List of uploaded files
        
    Returns:
        List of unique filenames
    """
    saved_filenames = []
    
    try:
        for file in files:
            filename = await save_image_file(file)
            saved_filenames.append(filename)
    except Exception as e:
        # If any file fails, clean up already saved files
        for filename in saved_filenames:
            file_path = UPLOAD_DIR / filename
            file_path.unlink(missing_ok=True)
        raise e
    
    return saved_filenames


def delete_image_file(filename: str) -> None:
    """Delete an image file from the filesystem."""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        file_path.unlink()


def get_image_url(filename: str) -> str:
    """Get the URL path for an image file."""
    return f"/static/images/{filename}"

