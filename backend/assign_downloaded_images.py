#!/usr/bin/env python3
"""
Assign downloaded images to apartments

This script takes images from the uploads directory and assigns them to apartments.
"""

import os
from pathlib import Path
from app.database.database import SessionLocal
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB
from app.utils.image_upload import UPLOAD_DIR

def assign_images_to_apartments(images_per_apartment: int = 4):
    """Assign downloaded images to apartments."""
    db = SessionLocal()
    
    try:
        # Get all image files from uploads directory
        image_files = [f.name for f in UPLOAD_DIR.glob("*") if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
        
        if not image_files:
            print("❌ No images found in uploads directory")
            return
        
        print(f"📁 Found {len(image_files)} image(s) in uploads directory")
        print()
        
        # Get all apartments
        apartments = db.query(ApartmentDB).all()
        
        if not apartments:
            print("❌ No apartments found in database")
            return
        
        print(f"🏠 Found {len(apartments)} apartment(s)")
        print()
        
        # Distribute images across apartments
        image_index = 0
        assigned_count = 0
        
        for apartment in apartments:
            # Get images for this apartment
            apartment_images = []
            for _ in range(images_per_apartment):
                if image_index >= len(image_files):
                    break
                apartment_images.append(image_files[image_index])
                image_index += 1
            
            if apartment_images:
                # Update apartment with new images
                apartment.images = apartment_images
                assigned_count += 1
                print(f"✅ Apartment {apartment.id}: Assigned {len(apartment_images)} image(s)")
        
        db.commit()
        
        print()
        print("=" * 60)
        print("📊 Summary")
        print("=" * 60)
        print(f"✅ Updated apartments: {assigned_count}")
        print(f"🖼️  Total images used: {image_index}")
        print(f"📁 Remaining images: {len(image_files) - image_index}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    assign_images_to_apartments(images_per_apartment=4)

