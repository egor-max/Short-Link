from collections.abc import Sequence
from uuid import UUID

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.links.generate_link import generate_short_link
from app.links.models import Link
from app.links.repositories import LinkRepositories
from app.links.schemas import (
    CreateLinkRequest,
    CreateLinkResponse,
    GetLinkResponse,
)


class LinkService:

    @classmethod
    async def add(
        cls,
        link_data: CreateLinkRequest,
        session: AsyncSession,
        request: Request,
    ) -> CreateLinkResponse:

        new_link = Link(
            links=str(link_data.link),
            short_links=generate_short_link(request),
        )

        result =  await LinkRepositories.create(new_link, session)

        return CreateLinkResponse(result)

    @classmethod
    async def get(
        cls,
        link_uuid: UUID,
        session: AsyncSession,
    ) -> GetLinkResponse:

        existing_link = await LinkRepositories.get(link_uuid, session)

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
    async def get_all(cls, session: AsyncSession) -> Sequence[GetLinkResponse]:

        return await LinkRepositories.get_all(session)

    @classmethod
    async def soft_delete(cls, link_uuid: UUID, session: AsyncSession) -> Response:

        existing_link = await LinkRepositories.get(link_uuid, session)

        if not existing_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Данная ссылка не найдена",
            )
        await LinkRepositories.soft_delete(existing_link, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @classmethod
    async def hard_delete(cls, link_uuid: UUID, session: AsyncSession) -> Response:

        existing_link = await LinkRepositories.get(link_uuid, session)

        if not existing_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Данная ссылка не найдена",
            )

        await LinkRepositories.hard_delete(existing_link, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @classmethod
    async def redirect(
        cls,
        short_link: UUID,
        session: AsyncSession,
        request: Request
    ) -> RedirectResponse:

        existing_link = await LinkRepositories.get_by_short_url(
            f"{request.base_url}/{short_link}",
            session,
        )

        if not existing_link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Данная ссылка не найдена",
            )
        return RedirectResponse(
            url=existing_link.link,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
