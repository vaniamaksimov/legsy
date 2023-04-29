from abc import ABC, abstractmethod
from http import HTTPStatus

import requests
from pydantic import BaseModel, ValidationError

from legsy.schemas import WBSchema
from legsy.core import exceptions

from .constants import HEADERS


class Parser(ABC):
    """Абстрактный базовый класс для парсеров данных."""
    headers = HEADERS
    encoding = 'utf-8'

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def parse(self) -> BaseModel:
        """Точка входа, возвращает Pydantic схему."""


class WBParser(Parser):
    """Парсер данных с сайта WB."""
    data_url = 'https://card.wb.ru/cards/detail?appType=1&curr=rub'\
               '&dest=-1257786&regions=80,64,38,4,115,83,33,68,70,'\
               '69,30,86,75,40,1,66,48,110,31,22,71,114&spp=0&nm='

    def __init__(self, nm_id: int) -> None:
        self.nm_id = nm_id
        self.data_url = self.data_url + str(nm_id)

    def get_data(self, response: requests.Response) -> dict:
        return response.json()

    def parse_data(self, data: dict) -> WBSchema:
        try:
            wbschema = WBSchema(**data)
            return wbschema
        except ValidationError as e:
            raise exceptions.ParseError(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Ошибка валидации данных: {e}'
            )

    def get_response(self) -> requests.Response:
        response = requests.get(
            url=self.data_url, headers=self.headers
        )
        response.encoding = self.encoding
        if response.status_code != HTTPStatus.OK:
            raise exceptions.ResponseStatusError(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    'Не удалось получить ответ с сервера WB '
                    ' статус ответа: {response.status_code}'
                )
            )
        return response

    def parse(self) -> WBSchema:
        response = self.get_response()
        data = self.get_data(response)
        json_schema = self.parse_data(data)
        return json_schema
