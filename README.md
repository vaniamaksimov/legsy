# Тестовое задание в компанию Legsy

Это веб-приложение на базе фреймворка FastAPI, предназначенное для парсинга и хранения данных с сайта wildberries. Приложение позволяет парсить карточку товара по артикулу и сохранять результат в базу данных, получать результат из базы данных по артикулу товара, получать список всех товаров из базы данных, удалять товар из базы данных по артикулу.

## Основные функциональности

- Парсинг: Приложение позволяет парсить данные с сайта wildberris.
- Хранение: Приложение позволяет хранить данные в базе данных.
- Работа с данными: Приложение позволяет получать и удалять данные из базы данных.


## Установка и запуск проекта

1. Клонирование репозитория: `git clone git@github.com:vaniamaksimov/legsy.git`
2. Переходим в папку с проектом командой `cd legsy`
3. Выполняем команду `mv .env-example .env`
4. Для разработки:
    - Устанавливаем зависимости с помощью poetry https://python-poetry.org/docs/basic-usage/
5. Для старта приложения:
    - Удаляем из .env файла DATABASE_URL
    - Переходим в папку infra `cd infra`
    - Выполняем команду `docker compose up`
    - Документация доступна по адресу http://localhost:8000/docs#/


## Технологии

Проект разработан с использованием следующих технологий и инструментов:

- FastAPI
- Pydantic
- Requests
- PostgreSQL
- Docker

## Автор

Иван Максимов (vaniamaksimov@gmail.com)
