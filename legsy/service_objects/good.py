from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from legsy.models import Good, GoodSize, GoodColor
from legsy.parser import WBParser
from legsy.schemas import (BrandCreate, ColorCreate, GoodCreate, GoodUpdate,
                           SizeCreate)

from .base import BaseServiceObject
from .brand import brand_service_object
from .color import color_service_object
from .size import size_service_object


class GoodServiceObject(BaseServiceObject[Good, GoodCreate, GoodUpdate]):

    async def create(self, schema: GoodCreate, session: AsyncSession) -> Good:
        json_schema = WBParser(schema.nm_id).parse()
        product_json_schema = json_schema.data.products[0]
        good = Good(
            nm_id=product_json_schema.nm_id,
            name=product_json_schema.name,
            supplier_id=product_json_schema.supplier_id,
            sale=product_json_schema.sale,
            price=product_json_schema.price,
            sale_price=product_json_schema.sale_price,
            rating=product_json_schema.rating,
            feedbacks=product_json_schema.feedbacks,
        )
        brand, created = await brand_service_object.get_or_create(
            BrandCreate(name=product_json_schema.brand,
                        brand_id=product_json_schema.brand_id,
                        site_brand_id=product_json_schema.site_brand_id),
            session,
        )
        good.brand = brand
        for color_schema in product_json_schema.colors:
            color, created = await color_service_object.get_or_create(
                ColorCreate(name=color_schema.name),
                session
            )
            goodcolor = GoodColor(good=good, color=color)
            good.colors.append(goodcolor)
        for size_schema in product_json_schema.sizes:
            size, created = await size_service_object.get_or_create(
                SizeCreate(name=size_schema.name),
                session,
            )
            goodsize = GoodSize(
                quantity=size_schema.stock,
                good=good,
                size=size,
            )
            good.sizes.append(goodsize)
        session.add(good)
        return good

    async def get_by_nm_id(
            self,
            obj_nm_id: int,
            session: AsyncSession,
    ) -> Good | None:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.nm_id == obj_nm_id
            )
        )
        return db_obj.scalars().first()

    async def get_or_create(
            self,
            obj_in: GoodCreate,
            session: AsyncSession
    ) -> tuple[Good, bool]:
        db_obj = await self.get_by_nm_id(obj_in.nm_id, session)
        if db_obj:
            return db_obj, False
        db_obj = await self.create(obj_in, session)
        return db_obj, True


good_service_object = GoodServiceObject(Good)
