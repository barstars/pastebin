from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select, inspect
from typing import Optional
from config import CONFIG
import asyncio

# Настройка БД
engine = create_async_engine("postgresql+asyncpg://{}:{}@{}/{}".format(CONFIG.get("username"), CONFIG.get("password"), CONFIG.get("server_ip"), CONFIG.get("database_name")))
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = "data"

    ip_address: Mapped[str]
    useragent: Mapped[str]
    url: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str]

    async def get_datas(self):
        return {"ip_address":self.ip_address, "useragent":self.useragent, "url":self.url, "text":self.text}

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

class DataManager:
    @classmethod
    async def create(cls):
        print("create method ranned!!!")
        await delete_tables()
        await create_tables()
        return cls()

    async def add(self, **data):
        async with SessionLocal() as session:
            session.add(Data(**data))
            await session.commit()

    async def if_url_exists(self, url: str) -> bool:
        async with SessionLocal() as session:
            result = await session.scalar(select(Data).where(Data.url == url))
            return result is not None

    async def read_text(self, url: str) -> Optional[str]:
        async with SessionLocal() as session:
            result = await session.scalar(select(Data).where(Data.url == url))
            return result.text if result else None

    async def read_from_useragent(self, useragent: str) -> Optional[dict]:
        async with SessionLocal() as session:
            result = await session.execute(select(Data).where(Data.useragent == useragent))
            curr = result.scalars().all()
            return [await row.get_datas() for row in curr]

    async def read_all(self):
        async with SessionLocal() as session:
            result = await session.execute(select(Data))
            curr = result.scalars().all()
            return [await row.get_datas() for row in curr]