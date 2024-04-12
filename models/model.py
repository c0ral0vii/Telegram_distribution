import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import func
from config.config import SQLACHEMY_URL

engine = create_async_engine(SQLACHEMY_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(unique=True)
    app_id: Mapped[int] = mapped_column(default=6)
    app_hash: Mapped[str] = mapped_column()
    device_model: Mapped[str] = mapped_column()
    app_version: Mapped[str] = mapped_column()

    proxy: Mapped[str] = mapped_column()
    created_at: Mapped[str] = mapped_column(default=datetime.datetime.now(
                                                        tz=datetime.timezone(
                                                            datetime.timedelta(hours=3)
                                                        )))

    status: Mapped[str] = mapped_column(default='Active')


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    from_account: Mapped[str] = mapped_column()

    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), default=func.now())


async def async_init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)