from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Handle None or empty string
if not DATABASE_URL:
    DATABASE_URL = "mysql+aiomysql://root:password@localhost/expense_tracker"

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"ssl": True} if "aivencloud.com" in DATABASE_URL else {}
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
