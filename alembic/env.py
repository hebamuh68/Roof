import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# --- Ensure project root is on sys.path ---
sys.path.append(str(Path(__file__).resolve().parents[1]))

# --- Load .env file ---
load_dotenv()

# --- Alembic Config object ---
config = context.config

# --- Logging setup ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Import DB Base and models ---
from app.database.database import Base
from app.schemas import user_sql, apartment_sql  # Import all models so Alembic can detect them

# --- Database URL from environment ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

# Set DB URL in Alembic config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# --- Metadata for autogenerate ---
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Run migrations ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
