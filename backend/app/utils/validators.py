"""
Input Validation Utilities.

Provides comprehensive validation functions for user inputs including
password strength, email domains, and profile completeness.
"""

import re
from typing import Dict, List, Optional, Tuple
from pydantic import EmailStr


# ===========================
# Password Validation
# ===========================

def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
    """
    Validate password strength against security requirements.

    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*(),.?":{}|<>)
    - No common passwords
    - No sequential characters (123, abc)

    Args:
        password: Password string to validate

    Returns:
        Tuple of (is_valid: bool, errors: List[str])

    Example:
        >>> is_valid, errors = validate_password_strength("weak")
        >>> print(errors)
        ['Password must be at least 8 characters', ...]
    """
    errors = []

    # Check minimum length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")

    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")

    # Check for digit
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")

    # Check for special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)")

    # Check for common passwords
    common_passwords = [
        'password', 'password123', '12345678', 'qwerty', 'abc123',
        'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
        'bailey', 'passw0rd', 'shadow', '123123', '654321'
    ]
    if password.lower() in common_passwords:
        errors.append("Password is too common. Please choose a more unique password")

    # Check for sequential characters
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        errors.append("Password should not contain sequential characters (e.g., 123, abc)")

    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        errors.append("Password should not contain more than 2 repeated characters")

    is_valid = len(errors) == 0
    return is_valid, errors


def get_password_strength_score(password: str) -> Dict[str, any]:
    """
    Calculate password strength score and provide feedback.

    Args:
        password: Password to evaluate

    Returns:
        dict: Contains score (0-100), strength level, and suggestions

    Example:
        >>> result = get_password_strength_score("MyP@ss123")
        >>> print(result['strength'])  # 'Strong'
        >>> print(result['score'])  # 85
    """
    score = 0
    suggestions = []

    # Length scoring
    length = len(password)
    if length >= 8:
        score += 20
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10
    else:
        suggestions.append("Consider using a longer password (12+ characters)")

    # Character variety scoring
    if re.search(r'[a-z]', password):
        score += 10
    else:
        suggestions.append("Add lowercase letters")

    if re.search(r'[A-Z]', password):
        score += 10
    else:
        suggestions.append("Add uppercase letters")

    if re.search(r'\d', password):
        score += 10
    else:
        suggestions.append("Add numbers")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 15
    else:
        suggestions.append("Add special characters")

    # Bonus for multiple character types
    char_types = sum([
        bool(re.search(r'[a-z]', password)),
        bool(re.search(r'[A-Z]', password)),
        bool(re.search(r'\d', password)),
        bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    ])
    if char_types >= 3:
        score += 15
    if char_types == 4:
        score += 10

    # Penalties
    if re.search(r'(.)\1{2,}', password):
        score -= 10
        suggestions.append("Avoid repeated characters")

    # Determine strength level
    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Medium"
    elif score >= 20:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return {
        "score": max(0, min(100, score)),
        "strength": strength,
        "suggestions": suggestions,
        "is_acceptable": score >= 40
    }


# ===========================
# Email Validation
# ===========================

def validate_email_domain(email: str, allowed_domains: Optional[List[str]] = None,
                         blocked_domains: Optional[List[str]] = None) -> Tuple[bool, Optional[str]]:
    """
    Validate email domain against allowed/blocked lists.

    Args:
        email: Email address to validate
        allowed_domains: List of allowed domains (if provided, only these are accepted)
        blocked_domains: List of blocked domains (these are rejected)

    Returns:
        Tuple of (is_valid: bool, error_message: Optional[str])

    Example:
        >>> is_valid, error = validate_email_domain(
        ...     "user@tempmail.com",
        ...     blocked_domains=["tempmail.com", "guerrillamail.com"]
        ... )
        >>> print(is_valid)  # False
    """
    # Default blocked domains (disposable email services)
    default_blocked_domains = [
        'tempmail.com', 'guerrillamail.com', 'mailinator.com',
        '10minutemail.com', 'throwaway.email', 'temp-mail.org',
        'fakeinbox.com', 'trashmail.com', 'yopmail.com',
        'getnada.com', 'maildrop.cc', 'sharklasers.com'
    ]

    # Basic email format validation
    if not email or '@' not in email:
        return False, "Invalid email format"

    parts = email.split('@')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return False, "Invalid email format"

    # Extract domain from email
    try:
        domain = parts[1].lower()
    except (IndexError, AttributeError):
        return False, "Invalid email format"

    # Check against allowed domains (if specified)
    if allowed_domains:
        if domain not in [d.lower() for d in allowed_domains]:
            return False, f"Email domain '{domain}' is not allowed. Please use an approved domain."

    # Check against blocked domains
    blocked = blocked_domains or []
    all_blocked = [d.lower() for d in default_blocked_domains + blocked]

    if domain in all_blocked:
        return False, f"Disposable email addresses are not allowed. Please use a permanent email address."

    return True, None


def is_business_email(email: str) -> bool:
    """
    Check if email appears to be a business/corporate email.

    Args:
        email: Email address to check

    Returns:
        bool: True if likely a business email

    Example:
        >>> is_business_email("user@company.com")  # True
        >>> is_business_email("user@gmail.com")  # False
    """
    common_consumer_domains = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'aol.com', 'icloud.com', 'mail.com', 'protonmail.com',
        'zoho.com', 'yandex.com'
    ]

    try:
        domain = email.split('@')[1].lower()
        return domain not in common_consumer_domains
    except (IndexError, AttributeError):
        return False


# ===========================
# Profile Completeness Validation
# ===========================

def validate_profile_completeness(user_data: dict, required_fields: Optional[List[str]] = None) -> Dict[str, any]:
    """
    Validate user profile completeness and calculate completion percentage.

    Args:
        user_data: Dictionary containing user profile data
        required_fields: Optional list of fields that must be filled

    Returns:
        dict: Contains completion_percentage, missing_fields, and is_complete

    Example:
        >>> user = {"first_name": "John", "email": "john@example.com"}
        >>> result = validate_profile_completeness(user)
        >>> print(result['completion_percentage'])  # 40
        >>> print(result['missing_fields'])  # ['last_name', 'location', ...]
    """
    # Define all profile fields and their weights
    profile_fields = {
        'first_name': 10,
        'last_name': 10,
        'email': 15,  # Critical field
        'location': 15,  # Important for apartment search
        'flatmate_pref': 10,
        'keywords': 10,
        'phone': 10,  # Optional but valuable
        'bio': 10,  # Optional
        'profile_picture': 10,  # Optional
        'verified_email': 10  # Security feature
    }

    # Required fields (must be filled for basic profile)
    default_required_fields = ['first_name', 'last_name', 'email', 'location']
    required = required_fields or default_required_fields

    # Calculate completion
    total_weight = sum(profile_fields.values())
    earned_weight = 0
    missing_fields = []
    missing_required_fields = []

    for field, weight in profile_fields.items():
        value = user_data.get(field)

        # Check if field is filled (properly)
        is_filled = False
        if isinstance(value, str):
            # String must have non-whitespace content
            is_filled = bool(value.strip())
        elif isinstance(value, list):
            # List must be non-empty
            is_filled = len(value) > 0
        elif isinstance(value, bool):
            # Boolean must be True
            is_filled = value
        elif value is not None:
            # Other non-None values count as filled
            is_filled = True

        if is_filled:
            earned_weight += weight
        else:
            missing_fields.append(field)
            if field in required:
                missing_required_fields.append(field)

    completion_percentage = int((earned_weight / total_weight) * 100)

    # Determine profile status
    if completion_percentage == 100:
        status = "Complete"
    elif completion_percentage >= 75:
        status = "Almost Complete"
    elif completion_percentage >= 50:
        status = "Partial"
    else:
        status = "Incomplete"

    return {
        "completion_percentage": completion_percentage,
        "status": status,
        "missing_fields": missing_fields,
        "missing_required_fields": missing_required_fields,
        "is_complete": len(missing_required_fields) == 0,
        "is_fully_complete": completion_percentage == 100
    }


def get_profile_completion_tips(user_data: dict) -> List[str]:
    """
    Get actionable tips to improve profile completion.

    Args:
        user_data: User profile data

    Returns:
        List of tip strings

    Example:
        >>> tips = get_profile_completion_tips({"first_name": "John"})
        >>> print(tips[0])  # "Add your last name to complete your profile"
    """
    tips = []

    if not user_data.get('last_name'):
        tips.append("Add your last name to complete your profile")

    if not user_data.get('location'):
        tips.append("Add your location to find apartments near you")

    if not user_data.get('flatmate_pref') or len(user_data.get('flatmate_pref', [])) == 0:
        tips.append("Specify your flatmate preferences to get better matches")

    if not user_data.get('keywords') or len(user_data.get('keywords', [])) == 0:
        tips.append("Add keywords about your interests and lifestyle")

    if not user_data.get('phone'):
        tips.append("Add a phone number so renters can contact you")

    if not user_data.get('bio'):
        tips.append("Write a short bio to tell others about yourself")

    if not user_data.get('profile_picture'):
        tips.append("Upload a profile picture to build trust")

    if not user_data.get('verified_email'):
        tips.append("Verify your email address to increase credibility")

    return tips


# ===========================
# Combined Validation
# ===========================

def validate_user_registration(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    location: Optional[str] = None
) -> Tuple[bool, List[str]]:
    """
    Comprehensive validation for user registration.

    Args:
        email: User's email address
        password: User's password
        first_name: User's first name
        last_name: User's last name
        location: User's location (optional)

    Returns:
        Tuple of (is_valid: bool, errors: List[str])

    Example:
        >>> is_valid, errors = validate_user_registration(
        ...     "user@example.com",
        ...     "weak",
        ...     "John",
        ...     "Doe"
        ... )
        >>> print(errors)  # List of validation errors
    """
    errors = []

    # Validate email domain
    email_valid, email_error = validate_email_domain(email)
    if not email_valid:
        errors.append(email_error)

    # Validate password strength
    password_valid, password_errors = validate_password_strength(password)
    if not password_valid:
        errors.extend(password_errors)

    # Validate names
    if not first_name or len(first_name.strip()) < 2:
        errors.append("First name must be at least 2 characters long")

    if not last_name or len(last_name.strip()) < 2:
        errors.append("Last name must be at least 2 characters long")

    # Validate location if provided
    if location and len(location.strip()) < 2:
        errors.append("Location must be at least 2 characters long")

    is_valid = len(errors) == 0
    return is_valid, errors
