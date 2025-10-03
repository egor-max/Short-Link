from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link
from app.repositories import LinkRepositories
from app.schemas import CreateLinkRequest, CreateLinkResponse, GetLinkResponse


class LinkService:
    @classmethod
    async def add_new_link(
        cls,
        link_data: CreateLinkRequest,
        session: AsyncSession,
    ) -> CreateLinkResponse:

        new_link = Link(links=link_data.link, short_links= "Лаваш.говядина.твоя.мама")

        result =  await LinkRepositories.create_new_link(new_link, session)

        return CreateLinkResponse(link=result.links, short_link=result.short_links)

    @classmethod
    async def get_current_link(
        cls,
        link_uuid: UUID,
        session: AsyncSession,
    ) -> GetLinkResponse:

        existing_link = await LinkRepositories.get_current_link(link_uuid, session)

        if not existing_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Данная ссылка не найдена",
            )

        return GetLinkResponse(
            uuid=existing_link.uuid,
            short_link=existing_link.short_links,
            link=existing_link.link,
        )

    @classmethod
    async def get_all_links(cls, session: AsyncSession) -> Sequence[GetLinkResponse]:

        return await LinkRepositories.get_all_links(session)

    @classmethod
    async def soft_delete_link(cls, link_uuid: UUID, session: AsyncSession) -> Response:
        existing_link = await LinkRepositories.get_current_link(link_uuid, session)

        if not existing_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Данная ссылка не найдена",
            )
        await LinkRepositories.soft_delete_link(existing_link, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @classmethod
    async def hard_delete_link(cls, link_uuid: UUID, session: AsyncSession) -> Response:
        existing_link = await LinkRepositories.get_current_link(link_uuid, session)

        if not existing_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Данная ссылка не найдена",
            )

        await LinkRepositories.hard_delete_link(existing_link, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
