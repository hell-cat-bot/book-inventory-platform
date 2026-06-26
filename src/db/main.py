from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.books.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


async_engine =create_async_engine(
    url = Config.DATABASE_URL,
    echo = True
)
    

async def init_db():
    async with async_engine.begin() as conn:
        from src.db.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)      # Only runs when no table present (also metadata.create_all requires a 'conn')


async def get_session() -> AsyncSession:
    #session class
    Session = sessionmaker(
        bind = async_engine,
        class_ = AsyncSession,
        expire_on_commit = False
    )

    #session obj
    async with Session() as session:
        yield session                  #its going to return our session 





#-----------------------------------conn vs session---------------------------------------------------
'''
Using async_engine.begin() works at the SQLAlchemy Core level, 
whereas using AsyncSession works at the ORM level(for CRUD)
'''

''' For Bulk Operations:

async def bulk_insert_books(books_list: list[dict]):
    # books_list is a list of raw dictionaries: [{"title": "Book 1", ...}, ...]
    async with async_engine.begin() as conn:
        await conn.execute(
            insert(Book),
            books_list
        )  # Directly runs a single, fast parameterized INSERT statement

'''

#--------------------------------run_migration_manually-----------------------------------------------
'''
import logging
from alembic import command
from alembic.config import Config

logger = logging.getLogger("uvicorn.error")

def run_alembic_migrations():
    logger.info("Running database migrations...")
    try:
        # 1. Point to your alembic.ini configuration file
        alembic_cfg = Config("alembic.ini")
        
        # 2. Programmatically execute 'alembic upgrade head'
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Database migrations applied successfully.")
    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")

--------------------------------------------------------------------------------

``` Since Alembic runs synchronously under the hood, so inside the "Startup Lifecycle" we 
    give it to 'anyio.to_thread' a worker thread
``` 

from fastapi import FastAPI
from contextlib import asynccontextmanager
import anyio

# Import your migration function
# from src.db.main import run_alembic_migrations 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run the synchronous migrations script in a separate thread
    await anyio.to_thread.run_sync(run_alembic_migrations)
    
    yield  # Web server starts running here
    
    # Cleanup on shutdown (if needed)

app = FastAPI(lifespan=lifespan)

-------------------------------------------------------------------------------
``` Alembic starts a conncection under the hood to do it (in alembic.ini)

connectable = async_engine_from_config(
    config.get_section(config.config_ini_section, {}),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

async with connectable.connect() as connection:
    await connection.run_sync(do_run_migrations)

---------------------------------------------------------------------------------
'''