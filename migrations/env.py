from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine
from dotenv import load_dotenv
import os

load_dotenv()

from hotels.models import Base as HotelBase
from booking.models import Base as BookingBase
from users.models import Base as UserBase

# Set up logging configuration
if context.config.config_file_name:
    fileConfig(context.config.config_file_name)

# Define target metadata
target_metadata = [HotelBase.metadata, BookingBase.metadata, UserBase.metadata]


# Define function to run migrations offline
def run_migrations_offline():
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Define function to run migrations online
def run_migrations_online():
    connectable = AsyncEngine(
        engine_from_config(
            context.config.get_section(context.config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Choose whether to run migrations offline or online based on configuration
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
