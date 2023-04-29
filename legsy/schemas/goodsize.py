from pydantic import BaseModel, Extra, Field, PositiveInt


class GoodSizeBase(BaseModel):
    quantity: int = Field(..., ge=0)

    class Config:
        extra = Extra.forbid


class GoodSizeCreate(GoodSizeBase):
    good_id: PositiveInt
    size_id: PositiveInt

    class Config(GoodSizeBase.Config):
        ...


class GoodSizeUpdate(GoodSizeBase):
    good_id: PositiveInt | None
    size_id: PositiveInt | None
    quantity: int | None = Field(0, ge=0)

    class Config(GoodSizeBase.Config):
        ...


class GoodSizeDB(BaseModel):
    id: int
    name: str
    quantity: int

    class Config:
        orm_mode = True
