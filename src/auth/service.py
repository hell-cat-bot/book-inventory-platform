from src.db.models import User
from .schemas import UserCreateModel
from .utils import generate_passwd_hash
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exist(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        # pops the unhashed-password out
        password = user_data_dict.pop("password")

        # hashes the password
        password_hash = generate_passwd_hash(password)

        # also provide the hased-password
        new_user = User(**user_data_dict, password_hash=password_hash)
        new_user.role = "user"

        session.add(new_user)

        await session.commit()

        return new_user
