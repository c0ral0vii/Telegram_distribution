from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.model import async_session, User


async def create_auth_user(user_id: int):
    async with async_session() as session:
        try:
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()
        except IntegrityError:
            await session.rollback()


async def get_root_accounts():
    async with async_session() as session:
        orders = await session.execute(User).scalars().all()
        print(orders)


async def check_account(user_id: int):
    async with async_session() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            return False
        return True
