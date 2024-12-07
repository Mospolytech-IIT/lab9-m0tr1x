"""This is the database module"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from models import Base

DATABASE_URL = "postgresql+asyncpg://mtrx@localhost:5432/postgres"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    """This function creates the tables in the database if they do not exist"""
    try:
        async with engine.begin() as conn:
            # Create all tables if they do not exist
            await conn.run_sync(Base.metadata.create_all)
            print("Tables created or already exist")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")

async def get_db() -> AsyncSession:
    """This function gets the db session"""
    async with SessionLocal() as session:
        yield session
