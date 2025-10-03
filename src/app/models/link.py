from sqlalchemy.orm import Mapped, mapped_column

from app.core import Base


class Link(Base):

    links: Mapped[str]
    short_links: Mapped[str]
    revoked: Mapped[bool] = mapped_column(default=False)
