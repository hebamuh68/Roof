from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# ===========================
# Password Hashing with bcrypt
# ===========================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Takes plain text password
    # Returns hashed version (safe to store in database)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Takes login password + stored hash
    # Returns True if password matches
    return pwd_context.verify(plain_password, hashed_password)


# ===========================
# JWT Token Creation
# ===========================

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM") 
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

def create_access_token(data: dict) -> str:
    # Takes user data (like email, user_id)
    # Returns JWT token string
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    # Takes JWT token
    # Returns user data if valid, raises error if invalid
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError("Invalid token")
        return {"email":email}
    except JWTError:
        raise JWTError("Invalid token")
    
def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token with longer expiration.

    Args:
        data: User data to encode (typically user_id and email)

    Returns:
        str: JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire, "type":"refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_refresh_token(token: str) -> dict:
    """
    Verify a refresh token and extract user data.

    Args:
        token: JWT refresh token

    Returns:
        dict: User data from token

    Raises:
        JWTError: If token is invalid or not a refresh token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verify it's a refresh token
        if payload.get("type") != "refresh":
            raise JWTError("Invalid token type")

        email: str = payload.get("sub")
        if email is None:
            raise JWTError("Invalid token")

        return {"email": email}
    except JWTError:
        raise JWTError("Invalid refresh token")