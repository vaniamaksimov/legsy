from http import HTTPStatus

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from legsy.schemas.WBJson import WBSchema, DataSchema, WBJsonProductSchema, SizeSchema, ColorSchema, ParamsSchema

from tests.fixtures.fixture_routes import (expected_data_list,
                                           expected_data_once,
                                           expected_deleted_data)


def test_good_list_get(client: TestClient, good):
    response = client.get('/goods')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_data_list


def test_post_with_already_in_base_dont_create_new_good(client: TestClient, good):
    response = client.post('/goods', json={'nm_id': 666})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_data_once
    response = client.get('/goods')
    assert response.json() == expected_data_list


def test_delete_object_by_client(client: TestClient, good):
    response = client.delete('/goods/666')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_deleted_data
    response = client.get('/goods')
    assert response.json() == []


def test_post_new_good_in_db(client: TestClient, monkeypatch: MonkeyPatch):
    def mocked_parse(self):
        return WBSchema(
            params=ParamsSchema(
                curr='rub'
            ),
            data=DataSchema(
                products=[
                    WBJsonProductSchema(
                        id=666,
                        name='Тестовый товар',
                        brand='Тестовый бренд',
                        brandId=666,
                        siteBrandId=666,
                        supplierId=666,
                        sale=666,
                        priceU=66600,
                        salePriceU=66600,
                        rating=666,
                        feedbacks=666,
                        colors=[
                            ColorSchema(
                                name='Тестовый цвет',
                            )
                        ],
                        sizes=[
                            SizeSchema(
                                name='Тестовый размер',
                                stocks=[
                                    {'qty': 666}
                                ]
                            )
                        ]
                    )
                ]
            )
        )
    monkeypatch.setattr('legsy.parser.parser.WBParser.parse', mocked_parse)
    response = client.post('/goods', json={"nm_id": 666})
    assert response.status_code == 200
    assert response.json() == expected_data_once
