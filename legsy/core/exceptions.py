from fastapi import HTTPException


class ParseError(HTTPException):
    """Базовый класс для ошибок парсера."""


class ResponseStatusError(HTTPException):
    """Статус ответа от сервера отличается от 200."""


class NoGoodInDbError(HTTPException):
    """Товар отсуствует в базе данных."""


class DBError(HTTPException):
    """Ошибка взаимодействия с базой данных."""
