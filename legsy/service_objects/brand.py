from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from legsy.models import Brand
from legsy.schemas import BrandCreate, BrandUpdate

from .base import BaseServiceObject


class BrandServiceObject(BaseServiceObject[Brand, BrandCreate, BrandUpdate]):

    async def get_by_brand_id(
            self,
            object_id: int,
            session: AsyncSession,
    ) -> Brand | None:
        db_obj = await session.execute(
            select(Brand).where(
                Brand.brand_id == object_id
            )
        )
        return db_obj.scalars().first()

    async def get_or_create(
            self,
            schema: BrandCreate,
            session: AsyncSession,
    ) -> tuple[Brand, bool]:
        db_obj = await self.get_by_brand_id(schema.brand_id, session)
        if db_obj:
            return db_obj, False
        db_obj = await self.create(schema, session)
        return db_obj, True


brand_service_object = BrandServiceObject(Brand)
