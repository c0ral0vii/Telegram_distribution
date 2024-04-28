import asyncio
import datetime


from models.model import Account, User, History, async_session
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from telethon import types


async def add_account(phone: str, proxy: str, app_hash: str, device_model: str, app_version: str):
    async with async_session() as session:
        try:
            account = Account(
                phone=phone,
                app_hash=app_hash,
                device_model=device_model,
                app_version=app_version,
                proxy=proxy,
            )

            session.add(account)

            await session.commit()
        except IntegrityError as e:
            await session.rollback()

async def get_accounts_db():
    async with async_session() as session:
        result = await session.execute(select(Account).where(Account.status == 'Active'))
        return result.scalars().all()


async def add_users(users: list or str):
    async with async_session() as session:
        try:
            if type(users) == int:
                model_user = User(
                    username=str(users)
                )
                session.add(model_user)
                await session.commit()
            else:
                for user in users:
                    if not user.bot and user.username is not None and user.photo is not None:
                        model_user = User(
                            username=user.username
                        )
                        session.add(model_user)
                        await session.commit()
        except IntegrityError as e:
            session.rollback()



async def change_status(banned: bool, phone: str):
    async with async_session() as session:
        if banned:
            account = await session.scalar(select(Account).where(Account.phone == phone))
            account.status = 'Banned'

            await session.commit()


async def get_users(count: int):
    async with async_session() as session:
        users = await session.execute(select(User).where(User.username is not None).limit(count))
        return users.scalars().all()


async def add_history(from_account: str, username: str):
    async with async_session() as session:
        history = History(
            from_account=from_account,
            username=username,
        )

        session.add(history)
        await session.commit()


async def delete_users():
    async with async_session() as session:
        try:
            await session.execute(delete(User))
            await session.commit()
        except Exception as e:
            await session.rollback()

async def delete_history():
    async with async_session() as session:
        try:
            await session.execute(delete(History))
            await session.commit()
        except Exception as e:
            await session.rollback()
