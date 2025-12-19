"""
Unit tests for validation utilities.

Tests password strength validation, email domain validation,
and profile completeness validation.
"""

import pytest
from app.utils.validators import (
    validate_password_strength,
    get_password_strength_score,
    validate_email_domain,
    is_business_email,
    validate_profile_completeness,
    get_profile_completion_tips,
    validate_user_registration
)


# ===========================
# Password Validation Tests
# ===========================

def test_password_strength_valid_strong_password():
    """Test that a strong password passes validation."""
    password = "MyStr0ng!Pass"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is True
    assert len(errors) == 0


def test_password_strength_too_short():
    """Test that short passwords are rejected."""
    password = "Short1!"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is False
    assert any("8 characters" in error for error in errors)


def test_password_strength_no_uppercase():
    """Test that passwords without uppercase are rejected."""
    password = "mypassword123!"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is False
    assert any("uppercase" in error.lower() for error in errors)


def test_password_strength_no_lowercase():
    """Test that passwords without lowercase are rejected."""
    password = "MYPASSWORD123!"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is False
    assert any("lowercase" in error.lower() for error in errors)


def test_password_strength_no_digit():
    """Test that passwords without digits are rejected."""
    password = "MyPassword!"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is False
    assert any("number" in error.lower() for error in errors)


def test_password_strength_no_special_char():
    """Test that passwords without special characters are rejected."""
    password = "MyPassword123"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is False
    assert any("special character" in error.lower() for error in errors)


def test_password_strength_common_password():
    """Test that common passwords are rejected."""
    common_passwords = ["password123", "12345678", "qwerty"]

    for password in common_passwords:
        is_valid, errors = validate_password_strength(password)
        assert is_valid is False
        assert any("common" in error.lower() for error in errors)


def test_password_strength_sequential_characters():
    """Test that passwords with sequential characters are rejected."""
    passwords_with_sequential = ["MyP@ss123word", "Abc!12345678"]

    for password in passwords_with_sequential:
        is_valid, errors = validate_password_strength(password)
        assert is_valid is False
        assert any("sequential" in error.lower() for error in errors)


def test_password_strength_repeated_characters():
    """Test that passwords with too many repeated characters are rejected."""
    password = "MyP@sssssword1"
    is_valid, errors = validate_password_strength(password)

    assert is_valid is False
    assert any("repeated" in error.lower() for error in errors)


def test_password_strength_score_weak():
    """Test password strength scoring for weak passwords."""
    password = "weak"
    result = get_password_strength_score(password)

    assert result['score'] < 40
    assert result['strength'] in ['Very Weak', 'Weak']
    assert result['is_acceptable'] is False
    assert len(result['suggestions']) > 0


def test_password_strength_score_medium():
    """Test password strength scoring for medium passwords."""
    password = "Pass12"  # 6 chars, has upper, lower, digit, but no special char and too short
    result = get_password_strength_score(password)

    # Should be medium strength (has variety but short)
    assert 40 <= result['score'] < 60
    assert result['strength'] == 'Medium'
    assert result['is_acceptable'] is True


def test_password_strength_score_strong():
    """Test password strength scoring for strong passwords."""
    password = "Str0ng!Password"
    result = get_password_strength_score(password)

    assert result['score'] >= 60
    assert result['strength'] in ['Strong', 'Very Strong']
    assert result['is_acceptable'] is True


def test_password_strength_score_very_strong():
    """Test password strength scoring for very strong passwords."""
    password = "V3ry!Str0ng#P@ssw0rd2024"
    result = get_password_strength_score(password)

    assert result['score'] >= 80
    assert result['strength'] == 'Very Strong'
    assert result['is_acceptable'] is True
    assert len(result['suggestions']) == 0 or len(result['suggestions']) == 1


# ===========================
# Email Validation Tests
# ===========================

def test_email_domain_valid():
    """Test that valid email domains pass validation."""
    email = "user@example.com"
    is_valid, error = validate_email_domain(email)

    assert is_valid is True
    assert error is None


def test_email_domain_disposable_blocked():
    """Test that disposable email addresses are blocked."""
    disposable_emails = [
        "user@tempmail.com",
        "user@guerrillamail.com",
        "user@mailinator.com"
    ]

    for email in disposable_emails:
        is_valid, error = validate_email_domain(email)
        assert is_valid is False
        assert "disposable" in error.lower()


def test_email_domain_custom_blocked():
    """Test custom blocked domains."""
    email = "user@blocked.com"
    is_valid, error = validate_email_domain(
        email,
        blocked_domains=["blocked.com"]
    )

    assert is_valid is False
    assert error is not None


def test_email_domain_allowed_list():
    """Test allowed domain list."""
    # Email in allowed list
    email1 = "user@company.com"
    is_valid1, error1 = validate_email_domain(
        email1,
        allowed_domains=["company.com", "business.com"]
    )
    assert is_valid1 is True

    # Email not in allowed list
    email2 = "user@other.com"
    is_valid2, error2 = validate_email_domain(
        email2,
        allowed_domains=["company.com", "business.com"]
    )
    assert is_valid2 is False


def test_email_domain_invalid_format():
    """Test invalid email format."""
    invalid_emails = ["notanemail", "user@", "@domain.com"]

    for email in invalid_emails:
        is_valid, error = validate_email_domain(email)
        assert is_valid is False
        assert "invalid" in error.lower()


def test_is_business_email():
    """Test business email detection."""
    # Consumer emails
    assert is_business_email("user@gmail.com") is False
    assert is_business_email("user@yahoo.com") is False
    assert is_business_email("user@hotmail.com") is False

    # Business emails
    assert is_business_email("user@company.com") is True
    assert is_business_email("user@mybusiness.org") is True


# ===========================
# Profile Completeness Tests
# ===========================

def test_profile_completeness_empty_profile():
    """Test completeness for empty profile."""
    user_data = {}
    result = validate_profile_completeness(user_data)

    assert result['completion_percentage'] == 0
    assert result['is_complete'] is False
    assert len(result['missing_required_fields']) > 0


def test_profile_completeness_minimal_profile():
    """Test completeness for minimal required profile."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "location": "New York"
    }
    result = validate_profile_completeness(user_data)

    assert result['completion_percentage'] >= 40
    assert result['is_complete'] is True  # Has all required fields
    assert len(result['missing_required_fields']) == 0


def test_profile_completeness_partial_profile():
    """Test completeness for partially filled profile."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "location": "New York",
        "flatmate_pref": ["non-smoker"]
    }
    result = validate_profile_completeness(user_data)

    assert 50 <= result['completion_percentage'] < 100
    assert result['status'] in ['Partial', 'Almost Complete']
    assert result['is_complete'] is True
    assert result['is_fully_complete'] is False


def test_profile_completeness_full_profile():
    """Test completeness for fully filled profile."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "location": "New York",
        "flatmate_pref": ["non-smoker", "quiet"],
        "keywords": ["netflix", "gym"],
        "phone": "1234567890",
        "bio": "Software developer",
        "profile_picture": "https://example.com/photo.jpg",
        "verified_email": True
    }
    result = validate_profile_completeness(user_data)

    assert result['completion_percentage'] == 100
    assert result['status'] == "Complete"
    assert result['is_complete'] is True
    assert result['is_fully_complete'] is True
    assert len(result['missing_fields']) == 0


def test_profile_completeness_missing_required_field():
    """Test that missing required fields are detected."""
    user_data = {
        "first_name": "John",
        "email": "john@example.com",
        # Missing: last_name, location
    }
    result = validate_profile_completeness(user_data)

    assert result['is_complete'] is False
    assert "last_name" in result['missing_required_fields']
    assert "location" in result['missing_required_fields']


def test_get_profile_completion_tips():
    """Test profile completion tips generation."""
    user_data = {
        "first_name": "John",
        "email": "john@example.com"
        # Missing most fields
    }

    tips = get_profile_completion_tips(user_data)

    assert len(tips) > 0
    assert any("last name" in tip.lower() for tip in tips)
    assert any("location" in tip.lower() for tip in tips)


def test_get_profile_completion_tips_complete_profile():
    """Test that complete profiles get minimal or no tips."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "location": "New York",
        "flatmate_pref": ["non-smoker"],
        "keywords": ["netflix"],
        "phone": "1234567890",
        "bio": "Developer",
        "profile_picture": "photo.jpg",
        "verified_email": True
    }

    tips = get_profile_completion_tips(user_data)

    assert len(tips) == 0  # Fully complete profile


# ===========================
# Combined Validation Tests
# ===========================

def test_validate_user_registration_success():
    """Test successful user registration validation."""
    is_valid, errors = validate_user_registration(
        email="user@example.com",
        password="MyStr0ng!Pass",
        first_name="John",
        last_name="Doe",
        location="New York"
    )

    assert is_valid is True
    assert len(errors) == 0


def test_validate_user_registration_weak_password():
    """Test registration with weak password."""
    is_valid, errors = validate_user_registration(
        email="user@example.com",
        password="weak",
        first_name="John",
        last_name="Doe"
    )

    assert is_valid is False
    assert len(errors) > 0
    assert any("password" in error.lower() for error in errors)


def test_validate_user_registration_disposable_email():
    """Test registration with disposable email."""
    is_valid, errors = validate_user_registration(
        email="user@tempmail.com",
        password="MyStr0ng!Pass",
        first_name="John",
        last_name="Doe"
    )

    assert is_valid is False
    assert any("disposable" in error.lower() for error in errors)


def test_validate_user_registration_short_name():
    """Test registration with too short name."""
    is_valid, errors = validate_user_registration(
        email="user@example.com",
        password="MyStr0ng!Pass",
        first_name="J",
        last_name="D"
    )

    assert is_valid is False
    assert any("at least 2 characters" in error for error in errors)


def test_validate_user_registration_all_invalid():
    """Test registration with all invalid inputs."""
    is_valid, errors = validate_user_registration(
        email="user@tempmail.com",
        password="weak",
        first_name="J",
        last_name="D"
    )

    assert is_valid is False
    assert len(errors) >= 3  # Multiple validation errors


# ===========================
# Edge Cases and Security Tests
# ===========================

def test_password_validation_unicode_characters():
    """Test password validation with unicode characters."""
    password = "MyP@ss123🔒"
    is_valid, errors = validate_password_strength(password)
    # Should still validate other requirements
    assert isinstance(is_valid, bool)


def test_email_domain_case_insensitive():
    """Test that email domain validation is case-insensitive."""
    email1 = "user@TEMPMAIL.COM"
    email2 = "user@TempMail.com"

    is_valid1, _ = validate_email_domain(email1)
    is_valid2, _ = validate_email_domain(email2)

    assert is_valid1 is False
    assert is_valid2 is False


def test_profile_completeness_empty_strings():
    """Test that empty strings don't count as filled fields."""
    user_data = {
        "first_name": "",
        "last_name": "   ",
        "email": "user@example.com",
        "location": ""
    }
    result = validate_profile_completeness(user_data)

    # Empty/whitespace strings should not count as filled
    assert "first_name" in result['missing_fields']
    assert "last_name" in result['missing_fields']
    assert "location" in result['missing_fields']


def test_profile_completeness_empty_arrays():
    """Test that empty arrays don't count as filled fields."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "location": "New York",
        "flatmate_pref": [],
        "keywords": []
    }
    result = validate_profile_completeness(user_data)

    assert "flatmate_pref" in result['missing_fields']
    assert "keywords" in result['missing_fields']
