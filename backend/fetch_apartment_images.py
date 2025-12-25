#!/usr/bin/env python3
"""
Fetch and Store Images for All Apartments

This script fetches images from the internet for all apartments in the database
and stores them locally, updating the apartment records with the image URLs.

Usage:
    python fetch_apartment_images.py [--unsplash-key KEY] [--images-per-apartment N]
    
Options:
    --unsplash-key: Unsplash API access key (optional, uses placeholder images if not provided)
    --images-per-apartment: Number of images to fetch per apartment (default: 4)
    --skip-existing: Skip apartments that already have images
"""

import os
import sys
import argparse
import requests
import uuid
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
import time

from app.database.database import SessionLocal
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB  # Import to resolve relationships
from app.utils.image_upload import UPLOAD_DIR, get_image_url


# Unsplash API configuration
UNSPLASH_API_URL = "https://api.unsplash.com"
UNSPLASH_SEARCH_ENDPOINT = f"{UNSPLASH_API_URL}/search/photos"

# Placeholder image service (no API key required)
PLACEHOLDER_IMAGE_SERVICE = "https://picsum.photos"

# Image dimensions
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600


def get_unsplash_images(query: str, count: int, access_key: Optional[str]) -> List[str]:
    """
    Fetch image URLs from Unsplash API based on search query.
    Focuses on apartment and interior photography.
    
    Args:
        query: Search query (e.g., "apartment interior", "living room")
        count: Number of images to fetch
        access_key: Unsplash API access key
        
    Returns:
        List of image URLs
    """
    if not access_key:
        return []
    
    try:
        headers = {
            "Authorization": f"Client-ID {access_key}"
        }
        params = {
            "query": query,
            "per_page": min(count, 30),  # Unsplash max is 30 per page
            "orientation": "landscape",
            # Add content filter to prefer interior/housing photos
            "content_filter": "high"  # Higher quality, more relevant results
        }
        
        response = requests.get(UNSPLASH_SEARCH_ENDPOINT, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        image_urls = []
        
        for photo in data.get("results", [])[:count]:
            # Get regular size image URL (800px width, good quality)
            if "urls" in photo and "regular" in photo["urls"]:
                image_urls.append(photo["urls"]["regular"])
        
        return image_urls
    
    except Exception as e:
        print(f"  ⚠️  Error fetching from Unsplash: {e}")
        return []


def get_placeholder_images(count: int) -> List[str]:
    """
    Get placeholder image URLs. 
    Note: Picsum provides random images, not apartment-specific.
    For better results, use Unsplash API with an access key.
    
    Args:
        count: Number of images to get
        
    Returns:
        List of placeholder image URLs
    """
    print("  ⚠️  Using placeholder images (random, not apartment-specific)")
    print("  💡 Tip: Use --unsplash-key for actual apartment interior images")
    
    image_urls = []
    for i in range(count):
        # Use different seed for each image to get variety
        seed = uuid.uuid4().int % 1000
        url = f"{PLACEHOLDER_IMAGE_SERVICE}/seed/{seed}/{IMAGE_WIDTH}/{IMAGE_HEIGHT}"
        image_urls.append(url)
    
    return image_urls


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
        response = requests.get(url, timeout=15, stream=True)
        response.raise_for_status()
        
        # Check if it's actually an image
        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            print(f"    ⚠️  URL does not point to an image: {content_type}")
            return False
        
        # Determine file extension from content type
        ext_map = {
            "image/jpeg": ".jpg",
            "image/jpg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp"
        }
        ext = ext_map.get(content_type, ".jpg")
        
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


def generate_search_queries(apartment: ApartmentDB) -> List[str]:
    """
    Generate search queries based on apartment properties.
    Focuses on apartment interior images: rooms, living spaces, kitchens, etc.
    
    Args:
        apartment: Apartment database object
        
    Returns:
        List of search query strings focused on apartment interiors
    """
    queries = []
    
    # Room-specific queries for different apartment types
    room_queries = {
        "Studio": [
            "studio apartment interior",
            "small apartment living room",
            "studio room design",
            "compact apartment",
            "efficiency apartment"
        ],
        "1BHK": [
            "one bedroom apartment interior",
            "1 bedroom living room",
            "small apartment bedroom",
            "1 bedroom kitchen",
            "single bedroom apartment"
        ],
        "2BHK": [
            "two bedroom apartment interior",
            "2 bedroom living room",
            "family apartment interior",
            "2 bedroom kitchen",
            "two bedroom home"
        ],
        "3BHK": [
            "three bedroom apartment interior",
            "3 bedroom living room",
            "spacious apartment interior",
            "3 bedroom home",
            "large apartment living space"
        ],
        "4BHK": [
            "four bedroom apartment interior",
            "4 bedroom living room",
            "large apartment interior",
            "4 bedroom home",
            "spacious family apartment"
        ],
        "Shared": [
            "shared room interior",
            "shared apartment bedroom",
            "roommate room",
            "shared living space",
            "student room"
        ],
        "Penthouse": [
            "luxury penthouse interior",
            "modern penthouse living room",
            "luxury apartment interior",
            "high-end apartment",
            "penthouse design"
        ]
    }
    
    # Get apartment type-specific queries
    apt_type = apartment.apartment_type or "apartment"
    queries.extend(room_queries.get(apt_type, [
        "apartment interior",
        "modern apartment living room",
        "apartment bedroom",
        "apartment kitchen",
        "home interior design"
    ]))
    
    # Add specific room type queries (always include these for variety)
    room_types = [
        "apartment living room",
        "apartment bedroom",
        "apartment kitchen",
        "apartment bathroom",
        "modern apartment interior"
    ]
    queries.extend(room_types)
    
    # Add furnishing-related queries
    if apartment.furnishing_type:
        if "furnished" in apartment.furnishing_type.lower():
            queries.extend([
                "furnished apartment interior",
                "furnished living room",
                "furnished bedroom"
            ])
        else:
            queries.extend([
                "unfurnished apartment",
                "empty apartment interior",
                "apartment for rent"
            ])
    
    # Remove duplicates and return
    unique_queries = list(dict.fromkeys(queries))  # Preserves order
    return unique_queries[:8]  # Return up to 8 queries for better variety


def fetch_and_save_images_for_apartment(
    apartment: ApartmentDB,
    images_per_apartment: int,
    unsplash_key: Optional[str],
    skip_existing: bool = False
) -> List[str]:
    """
    Fetch and save images for a single apartment.
    
    Args:
        apartment: Apartment database object
        images_per_apartment: Number of images to fetch
        unsplash_key: Unsplash API key (optional)
        skip_existing: If True, skip apartments that already have images
        
    Returns:
        List of saved image filenames
    """
    # Skip if apartment already has images
    if skip_existing and apartment.images and len(apartment.images) >= images_per_apartment:
        print(f"  ⏭️  Skipping apartment {apartment.id} (already has {len(apartment.images)} images)")
        return []
    
    print(f"  📸 Fetching {images_per_apartment} images for apartment {apartment.id}: {apartment.title}")
    
    # Generate search queries
    queries = generate_search_queries(apartment)
    
    # Try to get images from Unsplash first
    image_urls = []
    if unsplash_key:
        print(f"  🔍 Searching Unsplash for: {', '.join(queries[:3])}...")
        for query in queries:
            if len(image_urls) >= images_per_apartment:
                break
            needed = images_per_apartment - len(image_urls)
            unsplash_urls = get_unsplash_images(query, needed, unsplash_key)
            image_urls.extend(unsplash_urls)
            if unsplash_urls:
                print(f"    ✅ Found {len(unsplash_urls)} images for '{query}'")
            time.sleep(0.5)  # Rate limiting for Unsplash (50 requests per hour for free tier)
    else:
        print("  ⚠️  No Unsplash API key provided - using random placeholder images")
        print("  💡 Get a free API key at https://unsplash.com/developers for apartment-specific images")
    
    # Fill remaining with placeholder images if needed (only if no Unsplash key)
    if len(image_urls) < images_per_apartment and not unsplash_key:
        needed = images_per_apartment - len(image_urls)
        placeholder_urls = get_placeholder_images(needed)
        image_urls.extend(placeholder_urls)
    
    # Limit to requested number
    image_urls = image_urls[:images_per_apartment]
    
    # Download and save images
    saved_filenames = []
    for i, url in enumerate(image_urls, 1):
        # Generate unique filename
        ext = Path(urlparse(url).path).suffix or ".jpg"
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            ext = ".jpg"
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        save_path = UPLOAD_DIR / unique_filename
        
        print(f"    [{i}/{len(image_urls)}] Downloading from {url[:50]}...")
        
        if download_image(url, save_path):
            saved_filenames.append(unique_filename)
            print(f"      ✅ Saved as {unique_filename}")
        else:
            print(f"      ❌ Failed to download")
        
        # Small delay to avoid overwhelming servers
        time.sleep(0.3)
    
    return saved_filenames


def main():
    """Main function to fetch images for all apartments."""
    parser = argparse.ArgumentParser(description="Fetch and store images for all apartments")
    parser.add_argument(
        "--unsplash-key",
        type=str,
        help="Unsplash API access key (get from https://unsplash.com/developers)",
        default=os.getenv("UNSPLASH_ACCESS_KEY")
    )
    parser.add_argument(
        "--images-per-apartment",
        type=int,
        default=4,
        help="Number of images to fetch per apartment (default: 4)"
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip apartments that already have images"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🏠 Apartment Image Fetcher")
    print("=" * 60)
    print(f"Images per apartment: {args.images_per_apartment}")
    print(f"Skip existing: {args.skip_existing}")
    print(f"Unsplash API: {'✅ Configured' if args.unsplash_key else '❌ Not configured (using placeholder images)'}")
    print("=" * 60)
    print()
    
    # Ensure upload directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Fetch all apartments
        apartments = db.query(ApartmentDB).all()
        total = len(apartments)
        
        if total == 0:
            print("❌ No apartments found in database.")
            return
        
        print(f"📊 Found {total} apartments in database")
        print()
        
        success_count = 0
        error_count = 0
        skipped_count = 0
        
        for i, apartment in enumerate(apartments, 1):
            print(f"[{i}/{total}] Processing apartment {apartment.id}...")
            
            try:
                saved_filenames = fetch_and_save_images_for_apartment(
                    apartment,
                    args.images_per_apartment,
                    args.unsplash_key,
                    args.skip_existing
                )
                
                if saved_filenames:
                    # Convert filenames to URLs
                    image_urls = [get_image_url(filename) for filename in saved_filenames]
                    
                    # Update apartment with new images
                    if apartment.images:
                        # Append to existing images
                        apartment.images = list(apartment.images) + image_urls
                    else:
                        # Set new images
                        apartment.images = image_urls
                    
                    db.commit()
                    print(f"  ✅ Successfully saved {len(saved_filenames)} images")
                    success_count += 1
                elif args.skip_existing:
                    skipped_count += 1
                else:
                    print(f"  ⚠️  No images were saved")
                    error_count += 1
            
            except Exception as e:
                print(f"  ❌ Error processing apartment {apartment.id}: {e}")
                db.rollback()
                error_count += 1
            
            print()
        
        # Summary
        print("=" * 60)
        print("📊 Summary")
        print("=" * 60)
        print(f"✅ Successfully processed: {success_count}")
        print(f"⏭️  Skipped: {skipped_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📁 Total apartments: {total}")
        print("=" * 60)
    
    finally:
        db.close()


if __name__ == "__main__":
    main()

