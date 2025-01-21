from flask import current_app
import sys
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from backend.app import create_app, db  # Updated import to include db

config = context.config

app = create_app()
with app.app_context():
    target_metadata = db.metadata  # Use db.metadata directly
    
    # Escape '%' by replacing with '%%'
    escaped_db_uri = app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%')
    config.set_main_option('sqlalchemy.url', escaped_db_uri)

# Interpret the config file for Python logging.
from logging.config import fileConfig
fileConfig(config.config_file_name)

def run_migrations_offline():
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

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()