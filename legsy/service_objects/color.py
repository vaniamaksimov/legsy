from legsy.models import Color
from legsy.schemas import ColorCreate, ColorUpdate

from .base import BaseServiceObject, GetByNameMixin


class ColorServiceObject(
    GetByNameMixin,
    BaseServiceObject[Color, ColorCreate, ColorUpdate]
):
    ...


color_service_object = ColorServiceObject(Color)
