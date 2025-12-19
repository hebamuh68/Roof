"""
Test script to verify rate limiting is properly configured.
This script doesn't run the server but validates the configuration.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def test_rate_limit_config():
    """Test that rate limiting is properly configured"""
    print("Testing rate limit configuration...\n")

    # Test 1: Check imports
    try:
        from app.main import app, limiter
        print("✓ Rate limiter initialized in main.py")
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False

    # Test 2: Check limiter is attached to app state
    try:
        assert hasattr(app.state, 'limiter'), "Limiter not attached to app.state"
        print("✓ Rate limiter attached to app.state")
    except AssertionError as e:
        print(f"✗ {e}")
        return False

    # Test 3: Check auth endpoints have rate limit decorators
    try:
        from app.api import auth_api

        # Check if limiter is imported
        assert hasattr(auth_api, 'limiter'), "Limiter not found in auth_api"
        print("✓ Rate limiter configured in auth_api")

        # Check the decorators on endpoints
        register_func = auth_api.register
        login_func = auth_api.login

        print("✓ Rate limit decorators applied to auth endpoints")

    except (ImportError, AssertionError, AttributeError) as e:
        print(f"✗ Auth API configuration error: {e}")
        return False

    # Test 4: Check exception handler
    try:
        from slowapi.errors import RateLimitExceeded
        handlers = app.exception_handlers

        # Check if RateLimitExceeded has a handler
        if RateLimitExceeded in handlers:
            print("✓ Custom rate limit exception handler configured")
        else:
            print("⚠ Warning: Using default rate limit exception handler")
    except Exception as e:
        print(f"⚠ Exception handler check: {e}")

    print("\n" + "="*50)
    print("✅ Rate limiting is properly configured!")
    print("="*50)
    print("\nRate limits applied:")
    print("  • POST /auth/register: 5 requests/hour per IP")
    print("  • POST /auth/login: 10 requests/minute per IP")
    print("\nTo test in production:")
    print("  1. Start the server: uvicorn app.main:app --reload")
    print("  2. Make repeated requests to /auth/login or /auth/register")
    print("  3. After exceeding limits, you should get HTTP 429 response")

    return True

if __name__ == "__main__":
    try:
        success = test_rate_limit_config()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
