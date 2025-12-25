#!/usr/bin/env python3
"""
Clean up old sample image paths from apartments

This script removes or replaces old sample image paths that start with /static/images/sample
from apartment records in the database.
"""

from app.database.database import SessionLocal
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB  # Import to resolve relationships

def cleanup_sample_images():
    """Remove old sample image paths from apartments."""
    db = SessionLocal()
    
    try:
        # Find all apartments
        apartments = db.query(ApartmentDB).all()
        
        updated_count = 0
        total_sample_images = 0
        
        for apartment in apartments:
            if not apartment.images:
                continue
            
            # Check if any images are old sample paths
            original_images = list(apartment.images) if apartment.images else []
            cleaned_images = []
            has_sample_images = False
            
            for img_url in original_images:
                if img_url and '/static/images/sample' in img_url:
                    has_sample_images = True
                    total_sample_images += 1
                    # Skip this old sample image
                else:
                    cleaned_images.append(img_url)
            
            # Update apartment if we removed sample images
            if has_sample_images:
                apartment.images = cleaned_images if cleaned_images else None
                updated_count += 1
                print(f"✅ Cleaned apartment {apartment.id}: {apartment.title}")
                print(f"   Removed {len(original_images) - len(cleaned_images)} sample image(s)")
                print(f"   Remaining images: {len(cleaned_images) if cleaned_images else 0}")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("📊 Cleanup Summary")
        print("=" * 60)
        print(f"✅ Updated apartments: {updated_count}")
        print(f"🗑️  Removed sample images: {total_sample_images}")
        print(f"📁 Total apartments checked: {len(apartments)}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during cleanup: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_sample_images()

