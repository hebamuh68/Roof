#!/usr/bin/env python3
"""
Download Images from Webpage URL

This script downloads all images from a given webpage URL and optionally
assigns them to apartments in the database.

Usage:
    python download_images_from_url.py <url> [--apartment-id ID] [--max-images N]
    
Examples:
    # Download images from a webpage
    python download_images_from_url.py https://example.com/apartment-photos
    
    # Download and assign to specific apartment
    python download_images_from_url.py https://example.com/apartment-photos --apartment-id 5
    
    # Download maximum 10 images
    python download_images_from_url.py https://example.com/apartment-photos --max-images 10
"""

import os
import sys
import argparse
import requests
import uuid
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin, urlparse
import re
from html.parser import HTMLParser

from app.database.database import SessionLocal
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB  # Import to resolve relationships
from app.utils.image_upload import UPLOAD_DIR, get_image_url

# Image dimensions
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600


class ImageExtractor(HTMLParser):
    """HTML parser to extract image URLs from HTML content."""
    
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.image_urls = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            # Check src attribute
            if 'src' in attrs_dict:
                img_url = attrs_dict['src']
                # Convert relative URLs to absolute
                absolute_url = urljoin(self.base_url, img_url)
                if self._is_valid_image_url(absolute_url):
                    self.image_urls.append(absolute_url)
            # Check srcset attribute (for responsive images)
            if 'srcset' in attrs_dict:
                srcset = attrs_dict['srcset']
                # Parse srcset (format: "url1 size1, url2 size2")
                for item in srcset.split(','):
                    url_part = item.strip().split()[0]
                    absolute_url = urljoin(self.base_url, url_part)
                    if self._is_valid_image_url(absolute_url) and absolute_url not in self.image_urls:
                        self.image_urls.append(absolute_url)
    
    def _is_valid_image_url(self, url: str) -> bool:
        """Check if URL points to a valid image."""
        # Check file extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # Check if it's a data URL (skip)
        if url.startswith('data:'):
            return False
        
        # Check extension
        if any(path.endswith(ext) for ext in valid_extensions):
            return True
        
        # Check if URL contains image-related keywords (common CDN patterns)
        if any(keyword in url.lower() for keyword in ['image', 'img', 'photo', 'picture', 'media']):
            return True
        
        return False


def extract_images_from_url(url: str) -> List[str]:
    """
    Extract all image URLs from a webpage.
    
    Args:
        url: Webpage URL to extract images from
        
    Returns:
        List of image URLs found on the page
    """
    try:
        print(f"📥 Fetching webpage: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"✅ Successfully fetched webpage ({len(response.content)} bytes)")
        
        # Parse HTML to extract images
        parser = ImageExtractor(url)
        parser.feed(response.text)
        
        # Also try regex as fallback for embedded images
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        regex_images = re.findall(img_pattern, response.text, re.IGNORECASE)
        
        # Combine and deduplicate
        all_images = list(set(parser.image_urls + regex_images))
        
        # Convert relative URLs to absolute
        absolute_images = []
        for img_url in all_images:
            if not img_url.startswith('http'):
                img_url = urljoin(url, img_url)
            if parser._is_valid_image_url(img_url):
                absolute_images.append(img_url)
        
        # Remove duplicates while preserving order
        unique_images = list(dict.fromkeys(absolute_images))
        
        print(f"🔍 Found {len(unique_images)} image(s) on the page")
        return unique_images
    
    except Exception as e:
        print(f"❌ Error fetching webpage: {e}")
        return []


def download_image(url: str, save_path: Path) -> bool:
    """
    Download an image from URL and save it to the filesystem.
    
    Args:
        url: Image URL to download
        save_path: Path where to save the image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            print(f"    ⚠️  URL does not point to an image: {content_type}")
            return False
        
        # Determine file extension from content type or URL
        ext_map = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif"
        }
        ext = ext_map.get(content_type, "")
        
        # If no extension from content type, try to get from URL
        if not ext:
            parsed_url = urlparse(url)
            path_ext = Path(parsed_url.path).suffix.lower()
            if path_ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
                ext = path_ext
            else:
                ext = ".jpg"  # Default
        
        # Update save_path with correct extension
        if save_path.suffix != ext:
            save_path = save_path.with_suffix(ext)
        
        # Download and save
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    
    except Exception as e:
        print(f"    ⚠️  Error downloading image: {e}")
        if save_path.exists():
            save_path.unlink()  # Clean up partial file
        return False


def download_images_from_url(
    url: str,
    max_images: Optional[int] = None,
    apartment_id: Optional[int] = None
) -> List[str]:
    """
    Download all images from a webpage URL.
    
    Args:
        url: Webpage URL containing images
        max_images: Maximum number of images to download (None = all)
        apartment_id: Optional apartment ID to assign images to
        
    Returns:
        List of saved image filenames
    """
    print("=" * 60)
    print("🖼️  Image Downloader from URL")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Max images: {max_images or 'All'}")
    if apartment_id:
        print(f"Apartment ID: {apartment_id}")
    print("=" * 60)
    print()
    
    # Ensure upload directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Extract image URLs from webpage
    image_urls = extract_images_from_url(url)
    
    if not image_urls:
        print("❌ No images found on the webpage")
        return []
    
    # Limit number of images if specified
    if max_images:
        image_urls = image_urls[:max_images]
        print(f"📊 Limiting to {max_images} image(s)")
    
    print()
    print(f"📥 Downloading {len(image_urls)} image(s)...")
    print()
    
    # Download images
    saved_filenames = []
    for i, img_url in enumerate(image_urls, 1):
        # Generate unique filename
        ext = Path(urlparse(img_url).path).suffix or ".jpg"
        if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            ext = ".jpg"
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        save_path = UPLOAD_DIR / unique_filename
        
        print(f"  [{i}/{len(image_urls)}] Downloading {img_url[:60]}...")
        
        if download_image(img_url, save_path):
            saved_filenames.append(unique_filename)
            print(f"      ✅ Saved as {unique_filename}")
        else:
            print(f"      ❌ Failed to download")
    
    print()
    
    # Assign to apartment if specified
    if apartment_id and saved_filenames:
        db = SessionLocal()
        try:
            apartment = db.query(ApartmentDB).filter(ApartmentDB.id == apartment_id).first()
            if apartment:
                # Convert filenames to URLs (just filenames, no prefix)
                image_urls = saved_filenames
                
                # Update apartment with new images
                if apartment.images:
                    # Append to existing images
                    apartment.images = list(apartment.images) + image_urls
                else:
                    # Set new images
                    apartment.images = image_urls
                
                db.commit()
                print(f"✅ Assigned {len(saved_filenames)} image(s) to apartment {apartment_id}")
            else:
                print(f"⚠️  Apartment {apartment_id} not found")
        except Exception as e:
            print(f"❌ Error assigning images to apartment: {e}")
            db.rollback()
        finally:
            db.close()
    
    # Summary
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    print(f"✅ Successfully downloaded: {len(saved_filenames)}")
    print(f"📁 Images saved to: {UPLOAD_DIR}")
    if saved_filenames:
        print(f"\nSaved files:")
        for filename in saved_filenames:
            print(f"  - {filename}")
    print("=" * 60)
    
    return saved_filenames


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Download images from a webpage URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all images from a webpage
  python download_images_from_url.py https://example.com/apartment-photos
  
  # Download and assign to apartment ID 5
  python download_images_from_url.py https://example.com/apartment-photos --apartment-id 5
  
  # Download maximum 10 images
  python download_images_from_url.py https://example.com/apartment-photos --max-images 10
        """
    )
    parser.add_argument(
        "url",
        type=str,
        help="Webpage URL containing images to download"
    )
    parser.add_argument(
        "--apartment-id",
        type=int,
        help="Optional apartment ID to assign downloaded images to"
    )
    parser.add_argument(
        "--max-images",
        type=int,
        help="Maximum number of images to download (default: all)"
    )
    
    args = parser.parse_args()
    
    download_images_from_url(
        args.url,
        max_images=args.max_images,
        apartment_id=args.apartment_id
    )


if __name__ == "__main__":
    main()

