import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from legsy.models import Color, Size
from legsy.schemas import SizeUpdate
from legsy.service_objects import (brand_service_object, color_service_object,
                                   size_service_object)


@pytest.mark.parametrize(
        argnames=['service_object', 'name', 'model'],
        argvalues=[
            ((size_service_object), ('Тестовый размер'), (Size)),
            ((color_service_object), ('Тестовый цвет'), (Color)),
        ]
)
async def test_service_object_get_by_name(size, color, model, service_object, name, async_session_maker: sessionmaker):
    session: AsyncSession = async_session_maker()
    db_object = await service_object.get_by_name(name, session)
    assert db_object
    assert db_object.name == name
    count = await session.scalar(
        select(func.count()).select_from(model)
    )
    assert count == 1
    await session.close()


async def test_size_service_object_delete(size, async_session_maker: sessionmaker):
    session: AsyncSession = async_session_maker()
    await size_service_object.remove(size, session)
    await session.commit()
    count = await session.scalar(
        select(func.count()).select_from(Size)
    )
    assert count == 0
    await session.close()


async def test_size_service_object_rename(size, async_session_maker: sessionmaker):
    session: AsyncSession = async_session_maker()
    await size_service_object.update(size, SizeUpdate(name='Новое название размера'), session)
    await session.commit()
    count = await session.scalar(
        select(func.count()).select_from(Size)
    )
    assert count == 1
    new_named_size = await session.execute(
        select(Size)
    )
    new_named_size = new_named_size.scalar_one()
    assert new_named_size.name == 'Новое название размера'
    await session.close()


async def test_size_service_object_get_by_id(size, async_session_maker: sessionmaker):
    session: AsyncSession = async_session_maker()
    db_size = await size_service_object.get(size.id, session)
    assert db_size.id == size.id
    await session.close()
