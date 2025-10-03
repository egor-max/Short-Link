from collections.abc import AsyncGenerator
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column

from app.const import POOL_RECYCLE, POOL_SIZE
from app.core.env import settings


@as_declarative()
class Base(AsyncAttrs):

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


engine = create_async_engine(
    settings.postgres_url,
    pool_recycle=POOL_RECYCLE,
    pool_size=POOL_SIZE,
    pool_pre_ping=True,
    echo=settings.app_debug,
)
AsyncSessionLocal = async_sessionmaker(bind=engine)


async def get_async_session() -> AsyncGenerator[AsyncSession]:

    async with AsyncSessionLocal() as async_session:
        yield async_session


DBSession = Annotated[AsyncSession, Depends(get_async_session)]
