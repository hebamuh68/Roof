from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api import apartment_api, search_api, user_api, auth_api, admin_api, message_api, notifications_api
from app.schemas import user_sql, apartment_sql  # Required for SQLAlchemy relationships
from app.utils.error_handler import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    create_error_response
)
from app.utils.logger import setup_logging, log_request
from dotenv import load_dotenv
import os
from pathlib import Path
import logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Custom rate limit error handler
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(
        f"Rate limit exceeded: {request.client.host if request.client else 'unknown'}",
        extra={"path": request.url.path, "method": request.method}
    )
    return create_error_response(
        message="Too many requests. Please try again later.",
        status_code=429,
        details={"retry_after": exc.retry_after},
        error_code="RATE_LIMIT_EXCEEDED"
    )

# Request logging middleware
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all HTTP requests and responses."""
    log_request(request)
    
    try:
        response = await call_next(request)
        log_request(request, response=response)
        return response
    except Exception as e:
        log_request(request, error=e)
        raise

# CORS for frontend dev server
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for image serving
# Use the static/images directory in the backend folder
STATIC_IMAGES_DIR = Path(__file__).parent.parent / "static" / "images"
STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static/images", StaticFiles(directory=str(STATIC_IMAGES_DIR)), name="images")

app.include_router(search_api.router)
app.include_router(apartment_api.router)
app.include_router(user_api.router)
app.include_router(auth_api.router)
app.include_router(admin_api.router)
app.include_router(message_api.router)
app.include_router(notifications_api.router)