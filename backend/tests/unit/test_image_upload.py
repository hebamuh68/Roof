import pytest
from unittest.mock import Mock, patch, mock_open, MagicMock
from fastapi import UploadFile, HTTPException, status
from pathlib import Path
import os
import tempfile
import shutil

from app.utils.image_upload import (
    get_unique_filename,
    validate_image_file,
    save_image_file,
    save_multiple_images,
    delete_image_file,
    get_image_url,
    ALLOWED_CONTENT_TYPES,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE
)


class TestImageUpload:
    """Test suite for image upload utility functions."""

    def test_get_unique_filename_valid_extension(self):
        """Test generating unique filename with valid extension."""
        # Act
        filename = get_unique_filename("test.jpg")

        # Assert
        assert filename.endswith(".jpg")
        assert len(filename) == 36 + 4  # UUID hex (32) + .jpg (4)
        assert filename != "test.jpg"  # Should be unique

    def test_get_unique_filename_png(self):
        """Test generating unique filename for PNG."""
        # Act
        filename = get_unique_filename("image.png")

        # Assert
        assert filename.endswith(".png")

    def test_get_unique_filename_webp(self):
        """Test generating unique filename for WebP."""
        # Act
        filename = get_unique_filename("photo.webp")

        # Assert
        assert filename.endswith(".webp")

    def test_get_unique_filename_invalid_extension(self):
        """Test generating unique filename with invalid extension raises error."""
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            get_unique_filename("test.txt")
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid file extension" in exc.value.detail

    def test_get_unique_filename_case_insensitive(self):
        """Test that extension case doesn't matter."""
        # Act
        filename1 = get_unique_filename("test.JPG")
        filename2 = get_unique_filename("test.jpg")

        # Assert
        assert filename1.endswith(".jpg")
        assert filename2.endswith(".jpg")

    def test_validate_image_file_valid_jpeg(self):
        """Test validation of valid JPEG file."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "image/jpeg"
        mock_file.filename = "test.jpg"

        # Act & Assert - Should not raise
        validate_image_file(mock_file)

    def test_validate_image_file_valid_png(self):
        """Test validation of valid PNG file."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "image/png"
        mock_file.filename = "test.png"

        # Act & Assert - Should not raise
        validate_image_file(mock_file)

    def test_validate_image_file_valid_webp(self):
        """Test validation of valid WebP file."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "image/webp"
        mock_file.filename = "test.webp"

        # Act & Assert - Should not raise
        validate_image_file(mock_file)

    def test_validate_image_file_invalid_content_type(self):
        """Test validation fails for invalid content type."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "text/plain"
        mock_file.filename = "test.txt"

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            validate_image_file(mock_file)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid image type" in exc.value.detail

    def test_validate_image_file_no_filename(self):
        """Test validation fails when filename is missing."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "image/jpeg"
        mock_file.filename = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            validate_image_file(mock_file)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "No filename provided" in exc.value.detail

    def test_validate_image_file_invalid_extension(self):
        """Test validation fails for invalid file extension."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "image/jpeg"
        mock_file.filename = "test.gif"

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            validate_image_file(mock_file)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid file extension" in exc.value.detail

    @pytest.mark.asyncio
    async def test_save_image_file_success(self):
        """Test successfully saving an image file."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('app.utils.image_upload.UPLOAD_DIR', Path(temp_dir)):
                mock_file = Mock(spec=UploadFile)
                mock_file.content_type = "image/jpeg"
                mock_file.filename = "test.jpg"
                mock_file.seek = Mock()
                
                # Create small image data
                image_data = b"fake image data" * 100  # Small file
                mock_file.read = Mock(return_value=image_data)
                mock_file.read.side_effect = [image_data, b""]  # First read returns data, second returns empty

                # Act
                filename = await save_image_file(mock_file)

                # Assert
                assert filename is not None
                assert filename.endswith(".jpg")
                assert (Path(temp_dir) / filename).exists()
                mock_file.seek.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_image_file_too_large(self):
        """Test saving file that exceeds size limit."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('app.utils.image_upload.UPLOAD_DIR', Path(temp_dir)):
                mock_file = Mock(spec=UploadFile)
                mock_file.content_type = "image/jpeg"
                mock_file.filename = "test.jpg"
                mock_file.seek = Mock()
                
                # Create oversized data
                large_chunk = b"x" * (MAX_FILE_SIZE + 1)
                mock_file.read = Mock(return_value=large_chunk)

                # Act & Assert
                with pytest.raises(HTTPException) as exc:
                    await save_image_file(mock_file)
                assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
                assert "exceeds maximum" in exc.value.detail.lower()

    @pytest.mark.asyncio
    async def test_save_image_file_validation_error(self):
        """Test saving file with validation error."""
        # Arrange
        mock_file = Mock(spec=UploadFile)
        mock_file.content_type = "text/plain"
        mock_file.filename = "test.txt"

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            await save_image_file(mock_file)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_save_multiple_images_success(self):
        """Test successfully saving multiple images."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('app.utils.image_upload.UPLOAD_DIR', Path(temp_dir)):
                mock_file1 = Mock(spec=UploadFile)
                mock_file1.content_type = "image/jpeg"
                mock_file1.filename = "test1.jpg"
                mock_file1.seek = Mock()
                mock_file1.read = Mock(side_effect=[b"data1", b""])

                mock_file2 = Mock(spec=UploadFile)
                mock_file2.content_type = "image/png"
                mock_file2.filename = "test2.png"
                mock_file2.seek = Mock()
                mock_file2.read = Mock(side_effect=[b"data2", b""])

                # Act
                filenames = await save_multiple_images([mock_file1, mock_file2])

                # Assert
                assert len(filenames) == 2
                assert all(f.endswith((".jpg", ".png")) for f in filenames)
                assert all((Path(temp_dir) / f).exists() for f in filenames)

    @pytest.mark.asyncio
    async def test_save_multiple_images_cleanup_on_failure(self):
        """Test that failed uploads are cleaned up."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('app.utils.image_upload.UPLOAD_DIR', Path(temp_dir)):
                mock_file1 = Mock(spec=UploadFile)
                mock_file1.content_type = "image/jpeg"
                mock_file1.filename = "test1.jpg"
                mock_file1.seek = Mock()
                mock_file1.read = Mock(side_effect=[b"data1", b""])

                mock_file2 = Mock(spec=UploadFile)
                mock_file2.content_type = "text/plain"  # Invalid
                mock_file2.filename = "test2.txt"

                # Act & Assert
                with pytest.raises(HTTPException):
                    await save_multiple_images([mock_file1, mock_file2])

                # Verify first file was cleaned up
                files = list(Path(temp_dir).glob("*"))
                assert len(files) == 0

    def test_delete_image_file_exists(self):
        """Test deleting an existing image file."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.jpg"
            test_file.write_bytes(b"test data")

            with patch('app.utils.image_upload.UPLOAD_DIR', Path(temp_dir)):
                # Act
                delete_image_file("test.jpg")

                # Assert
                assert not test_file.exists()

    def test_delete_image_file_not_exists(self):
        """Test deleting non-existent file (should not raise)."""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('app.utils.image_upload.UPLOAD_DIR', Path(temp_dir)):
                # Act & Assert - Should not raise
                delete_image_file("nonexistent.jpg")

    def test_get_image_url(self):
        """Test generating image URL."""
        # Act
        url = get_image_url("test.jpg")

        # Assert
        assert url == "/static/images/test.jpg"

    def test_get_image_url_with_path(self):
        """Test generating image URL with path in filename."""
        # Act
        url = get_image_url("subfolder/test.jpg")

        # Assert
        assert url == "/static/images/subfolder/test.jpg"

