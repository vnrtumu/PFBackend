from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

import ssl

DATABASE_URL = os.getenv("DATABASE_URL")

# Handle None or empty string
if not DATABASE_URL:
    DATABASE_URL = "mysql+aiomysql://root:password@localhost/expense_tracker"

# Mask password for logging
masked_url = DATABASE_URL
if "@" in DATABASE_URL:
    parts = DATABASE_URL.split("@")
    prefix = parts[0].split("//")[0] + "//" + parts[0].split("//")[1].split(":")[0] + ":****"
    masked_url = prefix + "@" + parts[1]
print(f"Connecting to: {masked_url}")

ssl_ctx = None
if "aivencloud.com" in DATABASE_URL:
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    connect_args={"ssl": ssl_ctx} if ssl_ctx else {}
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
