import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from legsy.models import Brand, Color, Good, GoodColor, GoodSize, Size

pytest_plugins = [
    'tests.fixtures.fixture_core',
    'tests.fixtures.fixture_parser',
    'tests.fixtures.fixture_wbschema',
]


@pytest.fixture
async def size(async_session_maker: sessionmaker, db_session):
    session = async_session_maker()
    session: AsyncSession
    size = Size('Тестовый размер')
    session.add(size)
    await session.commit()
    await session.refresh(size)
    await session.close()
    return size


@pytest.fixture
async def color(async_session_maker: sessionmaker, db_session):
    session = async_session_maker()
    session: AsyncSession
    color = Color('Тестовый цвет')
    session.add(color)
    await session.commit()
    await session.refresh(color)
    await session.close()
    return color


@pytest.fixture
async def brand(async_session_maker: sessionmaker, db_session):
    session = async_session_maker()
    session: AsyncSession
    brand = Brand('Тестовый бренд', 666, 666)
    session.add(brand)
    await session.commit()
    await session.refresh(brand)
    await session.close()
    return brand


@pytest.fixture
async def good(async_session_maker: sessionmaker, db_session, size, brand, color):
    session = async_session_maker()
    session: AsyncSession
    good = Good(666, 'Тестовый товар', 666, 666, 666, 666, 666, 666, brand)
    goodcolor = GoodColor(good, color)
    good.colors.append(goodcolor)
    goodsize = GoodSize(666, good, size)
    good.sizes.append(goodsize)
    session.add(good)
    await session.commit()
    await session.refresh(good)
    await session.close()
    return good
