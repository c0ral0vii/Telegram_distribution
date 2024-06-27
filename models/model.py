import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Table, Column
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import func
from config.config import SQLACHEMY_URL

engine = create_async_engine(SQLACHEMY_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Proxy(Base):
    __tablename__ = 'proxys'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    proxy: Mapped[str] = mapped_column(nullable=False, unique=True)

    type: Mapped[str] = mapped_column(nullable=False, default='IPV6')

    account_id = mapped_column(ForeignKey('telegram_accounts.id'), nullable=False)
    account = relationship('TelegramAccount', back_populates='proxy')


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False, unique=True)


class TelegramAccount(Base):
    __tablename__ = "telegram_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(unique=True)
    app_id: Mapped[int] = mapped_column(default=6)
    app_hash: Mapped[str] = mapped_column()
    device_model: Mapped[str] = mapped_column()
    app_version: Mapped[str] = mapped_column()
    created_at: Mapped[str] = mapped_column(default=datetime.datetime.now(
                                                        tz=datetime.timezone(
                                                            datetime.timedelta(hours=3)
                                                        )))

    status: Mapped[str] = mapped_column(default='Неизвестен')
    spam_bot_status: Mapped[str] = mapped_column(nullable=False, default='Неизвестен')

    proxy = relationship('Proxy', back_populates='account')


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    sended: Mapped[str] = mapped_column(default=True)

    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), default=func.now())


async def async_init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)