#!/usr/bin/env python3
"""
Fix image URLs in database - remove /static/images/ prefix

This script removes the /static/images/ prefix from image URLs stored in the database,
so they're stored as just filenames. The API will add the prefix when serving.
"""

from app.database.database import SessionLocal
from app.schemas.apartment_sql import ApartmentDB
from app.schemas.user_sql import UserDB  # Import to resolve relationships

def fix_image_urls():
    """Remove /static/images/ prefix from image URLs in database."""
    db = SessionLocal()
    
    try:
        # Find all apartments
        apartments = db.query(ApartmentDB).all()
        
        updated_count = 0
        total_fixed = 0
        
        for apartment in apartments:
            if not apartment.images:
                continue
            
            # Check if any images have the /static/images/ prefix
            original_images = list(apartment.images) if apartment.images else []
            fixed_images = []
            needs_update = False
            
            for img_url in original_images:
                if not img_url:
                    continue
                
                # Remove /static/images/ prefix if present
                if img_url.startswith('/static/images/'):
                    # Extract just the filename
                    filename = img_url.replace('/static/images/', '')
                    fixed_images.append(filename)
                    needs_update = True
                    total_fixed += 1
                elif img_url.startswith('static/images/'):
                    # Handle case without leading slash
                    filename = img_url.replace('static/images/', '')
                    fixed_images.append(filename)
                    needs_update = True
                    total_fixed += 1
                else:
                    # Already just a filename, keep it
                    fixed_images.append(img_url)
            
            # Update apartment if we fixed any URLs
            if needs_update:
                apartment.images = fixed_images if fixed_images else None
                updated_count += 1
                print(f"✅ Fixed apartment {apartment.id}: {apartment.title}")
                print(f"   Fixed {len(original_images) - len([x for x in original_images if x and not x.startswith('/static/images/') and not x.startswith('static/images/')])} image URL(s)")
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("📊 Fix Summary")
        print("=" * 60)
        print(f"✅ Updated apartments: {updated_count}")
        print(f"🔧 Fixed image URLs: {total_fixed}")
        print(f"📁 Total apartments checked: {len(apartments)}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error during fix: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_image_urls()

