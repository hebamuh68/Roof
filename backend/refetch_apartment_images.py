#!/usr/bin/env python3
"""
Re-fetch apartment images with improved housing-specific queries

This script re-fetches images for all apartments using better search queries
focused on apartment interiors, rooms, and housing.

Usage:
    python refetch_apartment_images.py [--unsplash-key KEY] [--images-per-apartment N]
    
For best results, get a free Unsplash API key:
    1. Go to https://unsplash.com/developers
    2. Create a developer account
    3. Create a new application
    4. Copy your Access Key
    5. Run: python refetch_apartment_images.py --unsplash-key YOUR_KEY
"""

import sys
import os

# Import the fetch script functions
sys.path.insert(0, os.path.dirname(__file__))
from fetch_apartment_images import (
    main as fetch_main,
    SessionLocal,
    ApartmentDB,
    UserDB,
    fetch_and_save_images_for_apartment,
    UPLOAD_DIR,
    get_image_url
)
import argparse

def refetch_all_images(unsplash_key: str = None, images_per_apartment: int = 4):
    """Re-fetch images for all apartments, replacing existing ones."""
    print("=" * 60)
    print("🏠 Re-fetching Apartment Images")
    print("=" * 60)
    print(f"Images per apartment: {images_per_apartment}")
    print(f"Unsplash API: {'✅ Configured' if unsplash_key else '❌ Not configured'}")
    if not unsplash_key:
        print("⚠️  WARNING: Without Unsplash API key, you'll get random placeholder images")
        print("   Get a free key at: https://unsplash.com/developers")
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
        
        for i, apartment in enumerate(apartments, 1):
            print(f"[{i}/{total}] Processing apartment {apartment.id}...")
            
            try:
                # Clear existing images (we'll replace them)
                old_images = apartment.images
                apartment.images = None
                db.commit()
                
                # Fetch new images
                saved_filenames = fetch_and_save_images_for_apartment(
                    apartment,
                    images_per_apartment,
                    unsplash_key,
                    skip_existing=False  # Force re-fetch
                )
                
                if saved_filenames:
                    # Convert filenames to URLs (just filenames, no prefix)
                    image_urls = [filename for filename in saved_filenames]
                    
                    # Update apartment with new images
                    apartment.images = image_urls
                    
                    db.commit()
                    print(f"  ✅ Successfully replaced {len(saved_filenames)} images")
                    success_count += 1
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
        print(f"❌ Errors: {error_count}")
        print(f"📁 Total apartments: {total}")
        print("=" * 60)
    
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Re-fetch apartment images with improved queries")
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
    
    args = parser.parse_args()
    refetch_all_images(args.unsplash_key, args.images_per_apartment)

