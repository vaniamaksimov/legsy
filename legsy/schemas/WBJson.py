from typing import Literal

from pydantic import BaseModel, Field, validator, conlist


class ParamsSchema(BaseModel):
    curr: Literal['rub']


class ColorSchema(BaseModel):
    name: str


class SizeSchema(BaseModel):
    name: str
    stock: int = Field(alias='stocks')

    @validator('stock', pre=True)
    def summ_stocks(cls, value: list[dict[str, int]]):
        stock = sum([dct.get('qty') for dct in value])
        return stock

    @validator('name', pre=True)
    def name_validator(cls, value: str):
        return 'Без размера' if not value else value


class WBJsonProductSchema(BaseModel):
    nm_id: int = Field(alias='id')
    name: str
    brand: str
    brand_id: int = Field(alias='brandId')
    site_brand_id: int = Field(alias='siteBrandId')
    supplier_id: int = Field(alias='supplierId')
    sale: int
    price: int = Field(alias='priceU')
    sale_price: int = Field(alias='salePriceU')
    rating: int
    feedbacks: int
    colors: list[ColorSchema]
    sizes: conlist(SizeSchema, min_items=1)

    @validator('price', 'sale_price', pre=True)
    def normalize_price(cls, value: int):
        value = value / 100
        return value


class DataSchema(BaseModel):
    products: conlist(WBJsonProductSchema, min_items=1)


class WBSchema(BaseModel):
    params: ParamsSchema
    data: DataSchema
