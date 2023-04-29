from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from .brand import BrandDB
from .goodcolor import GoodColorDB
from .goodsize import GoodSizeDB


class GoodBase(BaseModel):
    nm_id: PositiveInt

    class Config:
        extra = Extra.forbid


class GoodCreate(BaseModel):
    nm_id: int


class GoodUpdate(GoodBase):
    name: str = Field(..., min_length=1, max_length=255,)

    @validator('name',)
    def not_null(cls, field: str | None) -> str:
        if field is None:
            raise ValueError('Cant be null')
        return field


class DeletedGoodDB(BaseModel):
    id: int
    nm_id: int
    name: str
    supplier_id: int
    sale: int
    price: int
    sale_price: int
    rating: int
    feedbacks: int

    class Config:
        orm_mode = True


class GoodDB(BaseModel):
    id: int
    nm_id: int
    name: str
    supplier_id: int
    sale: int
    price: int
    sale_price: int
    rating: int
    feedbacks: int
    brand: BrandDB
    colors: list[GoodColorDB]
    sizes: list[GoodSizeDB]

    class Config:
        orm_mode = True
