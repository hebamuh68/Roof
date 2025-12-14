import pytest
from datetime import datetime
from app.services.apartment_service import create_apartment, get_apartment_by_id, list_apartments, delete_apartment, update_apartment, get_my_apartments, get_my_apartments_count
from tests.factories.apartment_factory import ApartmentFactory
from app.models.apartment_pyd import ApartmentFilter, ApartmentRequest
from app.schemas.user_sql import UserDB, UserType
from app.schemas.apartment_sql import ApartmentDB


class TestApartmentService:
    """Test suite for apartment service CRUD operations."""

    def test_create_apartment_success(self, db_session):
        """Test successful apartment creation with valid data."""
        # Arrange
        apt_data = ApartmentFactory.build().__dict__
        req = ApartmentRequest(**apt_data)
        
        # Act
        apt = create_apartment(db_session, req)
        
        # Assert
        assert apt.id is not None
        assert apt.title == req.title
        assert apt.description == req.description
        assert apt.location == req.location
        assert apt.rent_per_week == req.rent_per_week
        assert apt.apartment_type == req.apartment_type
        assert apt.is_active == req.is_active
        # Verify it's persisted in database
        found_apt = get_apartment_by_id(db_session, apt.id)
        assert found_apt is not None
        assert found_apt.id == apt.id

    def test_create_apartment_with_minimal_data(self, db_session):
        """Test apartment creation with only required fields."""
        # Arrange
        minimal_data = {
            "title": "Minimal Apartment",
            "description": "Basic description", 
            "location": "Test City",
            "apartment_type": "Studio",
            "rent_per_week": 500,
            "start_date": datetime.utcnow(),
            "place_accept": "Students",
            "furnishing_type": "Furnished",
            "is_pathroom_solo": False,
            "parking_type": "None"
        }
        req = ApartmentRequest(**minimal_data)
        
        # Act
        apt = create_apartment(db_session, req)
        
        # Assert
        assert apt.id is not None
        assert apt.title == "Minimal Apartment"
        assert apt.is_active is True  # Default value

    def test_get_apartment_by_id_success(self, db_session, apartment_factory):
        """Test successful retrieval of apartment by ID."""
        # Arrange
        expected_title = "My Test Flat"
        apt = apartment_factory(title=expected_title)
        
        # Act
        found = get_apartment_by_id(db_session, apt.id)
        
        # Assert
        assert found is not None
        assert found.id == apt.id
        assert found.title == expected_title

    def test_get_apartment_by_id_not_found(self, db_session):
        """Test retrieval of non-existent apartment returns None."""
        # Act
        found = get_apartment_by_id(db_session, 99999)
        
        # Assert
        assert found is None

    def test_get_my_apartments(self, db_session):
        """Test getting apartments by renter."""
        # Arrange - Create two users
        user1 = UserDB(
            first_name="John",
            last_name="Doe",
            email="user1@test.com",
            location="New York",
            role=UserDB.__table__.c.role.type.python_type.RENTER,
            hashed_password="hashedpass123"
        )
        user2 = UserDB(
            first_name="Jane",
            last_name="Smith",
            email="user2@test.com",
            location="Los Angeles",
            role=UserDB.__table__.c.role.type.python_type.RENTER,
            hashed_password="hashedpass456"
        )
        db_session.add_all([user1, user2])
        db_session.commit()

        # Create apartments for user1
        apt1 = ApartmentDB(
            title="Apt 1",
            location="Brooklyn",
            apartment_type="Studio",
            rent_per_week=500,
            start_date=datetime.utcnow(),
            place_accept="Students",
            furnishing_type="Furnished",
            is_pathroom_solo=True,
            parking_type="Street",
            is_active=True,
            renter_id=user1.id
        )
        apt2 = ApartmentDB(
            title="Apt 2",
            location="Manhattan",
            apartment_type="1BHK",
            rent_per_week=800,
            start_date=datetime.utcnow(),
            place_accept="Professionals",
            furnishing_type="Semi-Furnished",
            is_pathroom_solo=False,
            parking_type="Garage",
            is_active=True,
            renter_id=user1.id
        )

        # Create apartment for user2
        apt3 = ApartmentDB(
            title="Apt 3",
            location="Santa Monica",
            apartment_type="2BHK",
            rent_per_week=1200,
            start_date=datetime.utcnow(),
            place_accept="Both",
            furnishing_type="Unfurnished",
            is_pathroom_solo=True,
            parking_type="Private",
            is_active=True,
            renter_id=user2.id
        )

        db_session.add_all([apt1, apt2, apt3])
        db_session.commit()

        # Act - Get user1's apartments
        my_apts = get_my_apartments(db_session, user1.id)

        # Assert
        assert len(my_apts) == 2
        assert all(apt.renter_id == user1.id for apt in my_apts)
        apartment_titles = [apt.title for apt in my_apts]
        assert "Apt 1" in apartment_titles
        assert "Apt 2" in apartment_titles
        assert "Apt 3" not in apartment_titles

    def test_get_my_apartments_with_pagination(self, db_session):
        """Test getting user's apartments with pagination."""
        # Arrange - Create a user
        user = UserDB(
            first_name="Test",
            last_name="User",
            email="testuser@test.com",
            location="Chicago",
            role=UserDB.__table__.c.role.type.python_type.RENTER,
            hashed_password="hashedpass"
        )
        db_session.add(user)
        db_session.commit()

        # Create 5 apartments for the user
        for i in range(5):
            apt = ApartmentDB(
                title=f"Apartment {i}",
                location="Test City",
                apartment_type="Studio",
                rent_per_week=500 + (i * 100),
                start_date=datetime.utcnow(),
                place_accept="Both",
                furnishing_type="Furnished",
                is_pathroom_solo=True,
                parking_type="None",
                is_active=True,
                renter_id=user.id
            )
            db_session.add(apt)
        db_session.commit()

        # Act - Get first page (2 items)
        page1 = get_my_apartments(db_session, user.id, skip=0, limit=2)

        # Act - Get second page (2 items)
        page2 = get_my_apartments(db_session, user.id, skip=2, limit=2)

        # Act - Get third page (remaining 1 item)
        page3 = get_my_apartments(db_session, user.id, skip=4, limit=2)

        # Assert
        assert len(page1) == 2
        assert len(page2) == 2
        assert len(page3) == 1

    def test_get_my_apartments_empty_result(self, db_session):
        """Test getting apartments for user with no apartments."""
        # Arrange - Create a user with no apartments
        user = UserDB(
            first_name="Empty",
            last_name="User",
            email="emptyuser@test.com",
            location="Boston",
            role=UserDB.__table__.c.role.type.python_type.RENTER,
            hashed_password="hashedpass"
        )
        db_session.add(user)
        db_session.commit()

        # Act
        my_apts = get_my_apartments(db_session, user.id)

        # Assert
        assert len(my_apts) == 0
        assert my_apts == []

    def test_get_my_apartments_count(self, db_session):
        """Test counting user's apartments."""
        # Arrange - Create a user
        user = UserDB(
            first_name="Count",
            last_name="Test",
            email="counttest@test.com",
            location="Seattle",
            role=UserDB.__table__.c.role.type.python_type.RENTER,
            hashed_password="hashedpass"
        )
        db_session.add(user)
        db_session.commit()

        # Create 3 apartments for the user
        for i in range(3):
            apt = ApartmentDB(
                title=f"Count Apartment {i}",
                location="Test City",
                apartment_type="Studio",
                rent_per_week=600,
                start_date=datetime.utcnow(),
                place_accept="Both",
                furnishing_type="Furnished",
                is_pathroom_solo=True,
                parking_type="None",
                is_active=True,
                renter_id=user.id
            )
            db_session.add(apt)
        db_session.commit()

        # Act
        count = get_my_apartments_count(db_session, user.id)

        # Assert
        assert count == 3

    def test_get_my_apartments_ordered_by_created_date(self, db_session):
        """Test that user's apartments are ordered by creation date (newest first)."""
        # Arrange - Create a user
        user = UserDB(
            first_name="Order",
            last_name="Test",
            email="ordertest@test.com",
            location="Portland",
            role=UserDB.__table__.c.role.type.python_type.RENTER,
            hashed_password="hashedpass"
        )
        db_session.add(user)
        db_session.commit()

        # Create apartments at different times
        from datetime import timedelta
        base_time = datetime.utcnow()

        apt_old = ApartmentDB(
            title="Oldest Apartment",
            location="Test City",
            apartment_type="Studio",
            rent_per_week=500,
            start_date=datetime.utcnow(),
            place_accept="Both",
            furnishing_type="Furnished",
            is_pathroom_solo=True,
            parking_type="None",
            is_active=True,
            created_at=base_time - timedelta(days=2),
            renter_id=user.id
        )
        apt_middle = ApartmentDB(
            title="Middle Apartment",
            location="Test City",
            apartment_type="Studio",
            rent_per_week=500,
            start_date=datetime.utcnow(),
            place_accept="Both",
            furnishing_type="Furnished",
            is_pathroom_solo=True,
            parking_type="None",
            is_active=True,
            created_at=base_time - timedelta(days=1),
            renter_id=user.id
        )
        apt_new = ApartmentDB(
            title="Newest Apartment",
            location="Test City",
            apartment_type="Studio",
            rent_per_week=500,
            start_date=datetime.utcnow(),
            place_accept="Both",
            furnishing_type="Furnished",
            is_pathroom_solo=True,
            parking_type="None",
            is_active=True,
            created_at=base_time,
            renter_id=user.id
        )

        db_session.add_all([apt_old, apt_middle, apt_new])
        db_session.commit()

        # Act
        my_apts = get_my_apartments(db_session, user.id)

        # Assert - Should be ordered newest first
        assert len(my_apts) == 3
        assert my_apts[0].title == "Newest Apartment"
        assert my_apts[1].title == "Middle Apartment"
        assert my_apts[2].title == "Oldest Apartment"

    def test_list_apartments_with_pagination(self, db_session, apartment_factory):
        """Test apartment listing with pagination parameters."""
        # Arrange
        apt1 = apartment_factory(title="Flat A")
        apt2 = apartment_factory(title="Flat B") 
        apt3 = apartment_factory(title="Flat C")
        
        # Act
        apts_page1 = list_apartments(db_session, skip=0, limit=2)
        apts_page2 = list_apartments(db_session, skip=2, limit=2)
        
        # Assert
        assert len(apts_page1) == 2
        assert len(apts_page2) == 1
        
        all_ids = [apt.id for apt in apts_page1 + apts_page2]
        assert apt1.id in all_ids
        assert apt2.id in all_ids 
        assert apt3.id in all_ids

    def test_list_apartments_empty_result(self, db_session):
        """Test listing apartments when none exist."""
        # Act
        apts = list_apartments(db_session)
        
        # Assert
        assert apts == []

    def test_list_apartments_default_pagination(self, db_session, apartment_factory):
        """Test listing apartments with default pagination values."""
        # Arrange - Create more than default limit
        for i in range(15):
            apartment_factory(title=f"Flat {i}")
        
        # Act
        apts = list_apartments(db_session)  # Uses defaults: skip=0, limit=10
        
        # Assert
        assert len(apts) == 10  # Should respect default limit

    def test_update_apartment_success(self, db_session, apartment_factory):
        """Test successful apartment update with valid data."""
        # Arrange
        original_title = "Old Title"
        original_rent = 800
        apt = apartment_factory(title=original_title, rent_per_week=original_rent)
        
        update_data = ApartmentFilter(
            title="New Updated Title", 
            rent_per_week=1200,
            description="Updated description"
        )
        
        # Act
        updated = update_apartment(db_session, apt.id, update_data)
        
        # Assert
        assert updated is not None
        assert updated.id == apt.id
        assert updated.title == "New Updated Title"
        assert updated.rent_per_week == 1200
        assert updated.description == "Updated description"
        # Verify unchanged fields remain the same
        assert updated.location == apt.location
        assert updated.apartment_type == apt.apartment_type

    def test_update_apartment_partial_update(self, db_session, apartment_factory):
        """Test partial update of apartment (only some fields)."""
        # Arrange
        apt = apartment_factory(title="Original", rent_per_week=800, location="Original City")
        update_data = ApartmentFilter(title="Updated Title Only")
        
        # Act
        updated = update_apartment(db_session, apt.id, update_data)
        
        # Assert
        assert updated.title == "Updated Title Only"
        assert updated.rent_per_week == 800  # Unchanged
        assert updated.location == "Original City"  # Unchanged

    def test_update_apartment_not_found(self, db_session):
        """Test updating non-existent apartment returns None."""
        # Arrange
        update_data = ApartmentFilter(title="New Title")
        
        # Act
        result = update_apartment(db_session, 99999, update_data)
        
        # Assert
        assert result is None

    def test_delete_apartment_success(self, db_session, apartment_factory):
        """Test successful apartment deletion."""
        # Arrange
        apt = apartment_factory(title="To Be Deleted")
        apt_id = apt.id
        
        # Act
        result = delete_apartment(db_session, apt_id)
        
        # Assert
        assert result == {"message": "Apartment deleted successfully"}
        # Verify it's actually deleted
        deleted_apt = get_apartment_by_id(db_session, apt_id)
        assert deleted_apt is None

    def test_delete_apartment_not_found(self, db_session):
        """Test deleting non-existent apartment returns None."""
        # Act
        result = delete_apartment(db_session, 99999)
        
        # Assert
        assert result is None