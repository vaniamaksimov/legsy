from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from .config import settings

engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as async_session:
        async_session: AsyncSession
        yield async_session
