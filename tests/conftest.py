import os
from typing import Any, Generator

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from legsy.core.base import Base
from legsy.core.session import get_async_session
from legsy.main import app

load_dotenv()

pytest_plugins = [
    'tests.fixtures.fixture_parser',
    'tests.fixtures.fixture_wbschema',
]


@pytest.fixture
def database_url() -> str:
    database_url = os.getenv('TEST_DATABASE_URL')
    return database_url


@pytest.fixture
def engine(database_url: str) -> AsyncEngine:
    engine = create_async_engine(
        url=database_url,
        connect_args={
            "check_same_thread": False
        }
    )
    return engine


@pytest.fixture
def async_session_maker(engine: AsyncEngine) -> sessionmaker:
    AsyncSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
    )
    return AsyncSessionLocal


@pytest.fixture
async def application(engine: AsyncEngine) -> Generator[FastAPI, Any, None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield app
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(
    application: FastAPI,
    engine: AsyncEngine,
    async_session_maker: sessionmaker
) -> Generator[AsyncSession, Any, None]:
    connection = await engine.connect()
    transaction = await connection.begin()
    session: AsyncSession = async_session_maker(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture()
def client(
    application: FastAPI,
    db_session: Generator[AsyncSession, Any, None],
) -> Generator[TestClient, Any, None]:

    async def override_get_async_session() -> AsyncSession:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    with TestClient(app=application) as client:
        yield client
