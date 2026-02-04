import os
from sqlmodel import SQLModel, create_engine, inspect
from backend.src.models import Task, User

# Use the same database URL as in the backend
database_url = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_7XRVveUNBG6r@ep-noisy-hall-ahm93msk-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')

# For PostgreSQL, we need to handle asyncpg driver differently
if database_url.startswith('postgresql'):
    # Replace postgresql+asyncpg with postgresql+psycopg2 for sync operations
    if '+asyncpg' in database_url:
        database_url = database_url.replace('+asyncpg', '+psycopg2')

engine = create_engine(database_url)

# Use SQLAlchemy's inspect to get table information
inspector = inspect(engine)

# Get columns for the task table
columns = inspector.get_columns('task')
print("Task table columns:")
for col in columns:
    print(f"  {col['name']}: {col['type']} (nullable: {col['nullable']})")

print("\nForeign key constraints:")
foreign_keys = inspector.get_foreign_keys('task')
for fk in foreign_keys:
    print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")