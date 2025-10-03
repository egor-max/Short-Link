from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, Response

from app.core import DBSession
from app.schemas import CreateLinkRequest, CreateLinkResponse, GetLinkResponse
from app.services import LinkService


router = APIRouter()

@router.post("/links")
async def add_link(
    link_data: CreateLinkRequest,
    session: DBSession,
) -> CreateLinkResponse:

    return await LinkService.add_new_link(link_data, session)

@router.get("/links/")
async def get_links(session: DBSession) -> Sequence[GetLinkResponse]:

    return await LinkService.get_all_links(session)

@router.get("/links/")
async def get_link(link_uuid: UUID, session: DBSession) -> GetLinkResponse:

    return await LinkService.get_current_link(link_uuid, session)


@router.delete("/links/")
async def soft_delete_link(link_uuid: UUID, session: DBSession) -> Response:
    return await LinkService.soft_delete_link(link_uuid, session)

@router.delete("/links/")
async def hard_delete_link(link_uuid: UUID, session: DBSession) -> Response:
    return await LinkService.hard_delete_link(link_uuid, session)
