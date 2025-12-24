"""
Logging configuration for the application.

This module sets up structured logging with appropriate handlers,
formatters, and log levels based on environment configuration.
"""

import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get log level from environment or default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_FILE = LOG_DIR / "app.log"
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB default
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# Create logs directory if it doesn't exist
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging():
    """
    Configure application-wide logging.

    Sets up:
    - Console handler with colored output for development
    - File handler with rotation for production
    - Structured format with timestamps, levels, and context
    - Appropriate log levels per environment
    """
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation (for production)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("elasticsearch").setLevel(logging.WARNING)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured - Level: {LOG_LEVEL}, File: {LOG_FILE}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Request logging middleware helper
def log_request(request, response=None, error=None):
    """
    Log HTTP request details.

    Args:
        request: FastAPI request object
        response: Response object (if available)
        error: Exception (if error occurred)
    """
    logger = logging.getLogger("http")
    
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "client": request.client.host if request.client else None,
    }

    if response:
        log_data["status_code"] = response.status_code
        logger.info(f"Request completed: {request.method} {request.url.path} - {response.status_code}")
    elif error:
        log_data["error"] = str(error)
        logger.error(f"Request failed: {request.method} {request.url.path} - {error}")
    else:
        logger.info(f"Request started: {request.method} {request.url.path}")

