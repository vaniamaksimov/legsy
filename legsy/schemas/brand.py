from pydantic import BaseModel, Extra, Field, PositiveInt

from legsy.core import settings


class BrandBase(BaseModel):
    name: str
    brand_id: int
    site_brand_id: int

    class Config:
        extra = Extra.forbid


class BrandCreate(BrandBase):
    name: str = Field(
        ...,
        min_length=settings.MIN_STRING_LENGTH,
        max_length=settings.MAX_STRING_LENGTH,
    )
    brand_id: PositiveInt
    site_brand_id: PositiveInt

    class Config(BrandBase.Config):
        ...


class BrandUpdate(BrandBase):
    name: str | None = Field(
        '',
        min_length=settings.MIN_STRING_LENGTH,
        max_length=settings.MAX_STRING_LENGTH,
    )
    brand_id: PositiveInt | None
    site_brand_id: PositiveInt | None

    class Config(BrandBase.Config):
        ...


class BrandDB(BaseModel):
    id: int
    name: str
    brand_id: int
    site_brand_id: int

    class Config:
        orm_mode = True
