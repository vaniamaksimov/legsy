from legsy.models import Size
from legsy.schemas import SizeCreate, SizeUpdate

from .base import BaseServiceObject, GetByNameMixin


class SizeServiceObject(
    GetByNameMixin,
    BaseServiceObject[Size, SizeCreate, SizeUpdate]
):
    ...


size_service_object = SizeServiceObject(Size)
