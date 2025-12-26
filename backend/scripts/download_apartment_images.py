#!/usr/bin/env python3
"""
Script to download apartment images from Unsplash and update the database.
Uses free stock images for apartment listings.
"""

import os
import sys
import uuid
import requests
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.schemas import apartment_sql, user_sql
from app.database.database import SessionLocal

# Directory for storing images
IMAGES_DIR = Path(__file__).parent.parent / "static" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Unsplash URLs for apartment images (various types)
APARTMENT_IMAGE_URLS = [
    # Living rooms
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&q=80",
    "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800&q=80",
    # Bedrooms
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80",
    "https://images.unsplash.com/photo-1616594039964-ae9021a400a0?w=800&q=80",
    "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&q=80",
    "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
    # Kitchens
    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80",
    "https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=800&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80",
    "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?w=800&q=80",
    # Bathrooms
    "https://images.unsplash.com/photo-1552321554-5fefe8c9ef14?w=800&q=80",
    "https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&q=80",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80",
    # Exteriors
    "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80",
    "https://images.unsplash.com/photo-1460317442991-0ec209397118?w=800&q=80",
    "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&q=80",
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80",
    # Modern apartments
    "https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?w=800&q=80",
    "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&q=80",
    "https://images.unsplash.com/photo-1600573472591-ee6c8e695f8a?w=800&q=80",
    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&q=80",
    # Studio apartments
    "https://images.unsplash.com/photo-1630699144867-37acec97df5a?w=800&q=80",
    "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800&q=80",
]


def download_image(url: str) -> str:
    """Download image from URL and save to static/images directory."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Generate unique filename
        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = IMAGES_DIR / filename

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"  Downloaded: {filename}")
        return filename
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return None


def main():
    print("Starting apartment image download...")
    print(f"Images will be saved to: {IMAGES_DIR}")

    # First, download all unique images
    print("\n1. Downloading images from Unsplash...")
    downloaded_images = []
    for i, url in enumerate(APARTMENT_IMAGE_URLS):
        print(f"  [{i+1}/{len(APARTMENT_IMAGE_URLS)}] Downloading...")
        filename = download_image(url)
        if filename:
            downloaded_images.append(filename)

    print(f"\nDownloaded {len(downloaded_images)} images")

    if not downloaded_images:
        print("No images were downloaded. Exiting.")
        return

    # Now update apartments in the database
    print("\n2. Updating apartments in database...")
    db = SessionLocal()

    try:
        apartments = db.query(apartment_sql.ApartmentDB).all()
        print(f"Found {len(apartments)} apartments to update")

        import random

        for apt in apartments:
            # Assign 3-5 random images to each apartment
            num_images = random.randint(3, min(5, len(downloaded_images)))
            apt_images = random.sample(downloaded_images, num_images)
            apt.images = apt_images
            print(f"  Apartment {apt.id}: assigned {len(apt_images)} images")

        db.commit()
        print("\nDatabase updated successfully!")

    except Exception as e:
        print(f"Error updating database: {e}")
        db.rollback()
    finally:
        db.close()

    print("\nDone!")


if __name__ == "__main__":
    main()
