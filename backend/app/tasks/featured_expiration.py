"""
Background task to expire featured apartments.
Run this as a cron job or scheduled task.

Usage:
    python -m app.tasks.featured_expiration

Cron example (run daily at midnight):
    0 0 * * * cd /path/to/backend && python -m app.tasks.featured_expiration
"""
from app.database.database import SessionLocal
from app.services import apartment_service


def expire_featured_apartments_task():
    """Expire featured apartments whose time has run out."""
    db = SessionLocal()
    try:
        count = apartment_service.expire_featured_apartments(db)
        print(f"Expired {count} featured apartments")
        return count
    finally:
        db.close()


if __name__ == "__main__":
    expire_featured_apartments_task()
