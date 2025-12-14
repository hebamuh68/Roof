"""
Apartment Utility Functions

This module provides utility functions for apartment-related operations
that are used across different parts of the application.

Functions:
    verify_apartment_ownership: Validate user ownership of an apartment
"""

from fastapi import HTTPException, status

from app.schemas.apartment_sql import ApartmentDB


def verify_apartment_ownership(apartment: ApartmentDB, user_id: int) -> None:
    """
    Verify that a user owns a specific apartment.

    Used as a security check before allowing update or delete operations.
    Raises an HTTP exception if the user doesn't own the apartment.

    Args:
        apartment: The apartment database object to verify
        user_id: The ID of the user claiming ownership

    Raises:
        HTTPException 403: If the user doesn't own the apartment

    Example:
        # In an API endpoint
        apartment = get_apartment_by_id(db, apartment_id)
        verify_apartment_ownership(apartment, current_user.id)
        # Proceed with update/delete if no exception raised

    Note:
        This function should be called BEFORE performing any modifications
        to ensure proper authorization.
    """
    if apartment.renter_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to modify this apartment. Only the apartment owner can perform this action."
        )
