from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.schemas import CreateLoginRequest


class UserRepositories:

    @classmethod
    async def add(cls, new_user: User, session: AsyncSession) -> User:
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)

        return new_user

    @classmethod
    async def login(
        cls,
        user_data: CreateLoginRequest,
        session: AsyncSession,
    ) -> User:

        stmt = select(User).where(User.email == user_data.email)
        result = session.execute(stmt)

        return await result

    @classmethod
    async def logout(cls) -> None:

        return None
