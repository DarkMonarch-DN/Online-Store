from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


engine = create_async_engine(
    url=settings.database.URL,
    echo=True,
    pool_size=10,           # Кол-во постоянных соединений
    max_overflow=20,        # Сколько доп. соединений можно открыть при пиках
    pool_timeout=30,        # Сколько секунд ждать свободного соединения
    pool_recycle=3600,      # Пересоздавать соединение раз в час (помогает от обрывов со стороны БД)
    pool_pre_ping=True      # Проверять соединение перед использованием («SELECT 1»)
)


async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session