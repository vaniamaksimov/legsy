from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from legsy.core import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class AbstractServiceObject(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType],
    ABC
):
    """Абстрактный класс для наследования сервисных объектов."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    @abstractmethod
    async def get(
        self,
        object_id: int,
        session: AsyncSession
    ) -> ModelType | None:
        """Получение объекта из базы данных по id."""

    @abstractmethod
    async def get_multi(
        self,
        session: AsyncSession
    ) -> list[ModelType | None]:
        """Получение списка объектов из базы данных."""

    @abstractmethod
    async def create(
            self,
            schema: CreateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        """Создание объекта в базе данных."""

    @abstractmethod
    async def update(
            self,
            database_object: ModelType,
            schema: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        """Обновление объекта в базе данных."""

    @abstractmethod
    async def remove(
            self,
            database_object: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        """Удаление объекта из базы данных."""


class BaseServiceObject(
    AbstractServiceObject[ModelType, CreateSchemaType, UpdateSchemaType]
):

    async def get(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> ModelType | None:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == object_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> list[ModelType | None]:
        db_objects = await session.execute(select(self.model))
        return db_objects.scalars().all()

    async def create(
            self,
            schema: CreateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        object_data = schema.dict()
        database_object = self.model(**object_data)
        session.add(database_object)
        return database_object

    async def update(
            self,
            database_object: ModelType,
            schema: UpdateSchemaType,
            session: AsyncSession,
    ) -> ModelType:
        object_data = jsonable_encoder(database_object)
        update_data = schema.dict(exclude_unset=True)
        for field_data_name in object_data:
            if field_data_name in update_data:
                setattr(database_object,
                        field_data_name,
                        update_data.get(field_data_name))
        session.add(database_object)
        return database_object

    async def remove(
            self,
            database_object: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        await session.delete(database_object)
        return database_object


class GetByNameMixin:
    """Миксин добавляющий методы get_by_name и get_or_create."""

    async def get_by_name(
            self: AbstractServiceObject,
            name: str,
            session: AsyncSession
    ):
        """Получение объекта но полю name."""
        database_object = await session.execute(
            select(self.model).where(
                self.model.name == name
            )
        )
        return database_object.scalars().first()

    async def get_or_create(
            self: AbstractServiceObject,
            schema: CreateSchemaType,
            session: AsyncSession
    ) -> tuple[ModelType, bool]:
        """Получение или создание объекта из базы даных."""
        db_obj = await self.get_by_name(schema.name, session)
        if db_obj:
            return db_obj, False
        db_obj = await self.create(schema, session)
        return db_obj, True
