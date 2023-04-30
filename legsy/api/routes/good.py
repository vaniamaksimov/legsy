from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from legsy.core import exceptions, get_async_session
from legsy.schemas import DeletedGoodDB, GoodCreate, GoodDB
from legsy.service_objects import good_service_object

router = APIRouter()


@router.get(
    path='/',
    response_model=list[GoodDB],
)
async def get_all_goods(
    session: AsyncSession = Depends(get_async_session),
):
    goods = await good_service_object.get_multi(session)
    return goods


@router.post(
    path='/',
    response_model=GoodDB,
)
async def create_good(
    good: GoodCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        good, created = await good_service_object.get_or_create(good, session)
        if created:
            await session.commit()
            await session.refresh(good)
        return good
    except SQLAlchemyError as e:
        raise exceptions.DBError(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Ошибка сохранения товара в базу данных. '
                f'{e._message()}'
            )
        )


@router.get(
    path='/{object_nm_id}',
    response_model=GoodDB,
)
async def get_good_by_nm_id(
    object_nm_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    good = await good_service_object.get_by_nm_id(object_nm_id, session)
    if good:
        return good
    raise exceptions.NoGoodInDbError(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=f'Товар с nm_id {object_nm_id} отуствует в базе данных.'
    )


@router.delete(
    path='/{object_nm_id}',
    response_model=DeletedGoodDB,
)
async def delete_good_by_nm_id(
    object_nm_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        good = await good_service_object.get_by_nm_id(object_nm_id, session)
        if good:
            deleted_good = await good_service_object.remove(good, session)
            await session.commit()
            return deleted_good
        raise exceptions.NoGoodInDbError(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Товар с nm_id {object_nm_id} отуствует в базе данных.'
        )
    except SQLAlchemyError as e:
        raise exceptions.DBError(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Ошибка удаления товара из базы данных. '
                f'{e._message()}'
            )
        )
