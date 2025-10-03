from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link


class LinkRepositories:
    @classmethod
    async def get_all_links(cls, session: AsyncSession) -> Sequence[Link]:
        stmt = select(Link)

        result = await session.execute(stmt)

        return result.scalars.all()

    @classmethod
    async def get_current_link(
        cls,
        link_uuid: UUID,
        session: AsyncSession,
    ) -> Link | None:
        stmt = select(Link).where(Link.uuid==link_uuid)

        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @classmethod
    async def create_new_link(cls, new_link: Link, session: AsyncSession) -> Link:
        session.add(new_link)

        await session.commit()
        await session.refresh(new_link)

        return new_link

    @classmethod
    async def soft_delete_link(cls, existing_link: Link, session: AsyncSession) -> None:
        existing_link.revoked = True

        session.add(existing_link)
        await session.commit()

    @classmethod
    async def hard_delete_link(cls, existing_link: Link, session: AsyncSession) -> None:
        session.delete(existing_link)
        await session.commit()
