from pydantic import BaseModel, Extra, PositiveInt


class GoodColorBase(BaseModel):
    good_id: PositiveInt
    color_id: PositiveInt

    class Config:
        extra = Extra.forbid


class GoodColorCreate(GoodColorBase):

    class Config(GoodColorBase.Config):
        ...


class GoodColorUpdate(GoodColorBase):
    good_id: PositiveInt | None
    color_id: PositiveInt | None

    class Config(GoodColorBase.Config):
        ...


class GoodColorDB(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
