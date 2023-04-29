from pydantic import BaseModel, Extra, Field, validator

from legsy.core import settings


class ColorBase(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid


class ColorCreate(ColorBase):
    name: str = Field(
        ...,
        min_length=settings.MIN_STRING_LENGTH,
        max_length=settings.MAX_STRING_LENGTH,
    )

    class Config(ColorBase.Config):
        ...


class ColorUpdate(ColorBase):
    name: str | None = Field(
        '',
        min_length=settings.MIN_STRING_LENGTH,
        max_length=settings.MAX_STRING_LENGTH,
    )

    @validator('name',)
    def not_null(cls, field: str | None) -> str:
        if field is None:
            raise ValueError('Cant be null')
        return field

    class Config(ColorBase.Config):
        ...


class ColorDB(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
