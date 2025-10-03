from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateLinkResponse(BaseModel):

    link: str
    short_link: str


class CreateLinkRequest(BaseModel):

    link: str


class GetLinkResponse(BaseModel):

    uuid: UUID
    link: str
    short_link: str

    model_config = ConfigDict(from_attributes=True)
