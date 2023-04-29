import pytest
from pytest import MonkeyPatch
from requests import Response

from legsy.core import exceptions
from legsy.parser import WBParser
from legsy.schemas import WBSchema


def test_init_parser(mocked_parser: WBParser):
    assert mocked_parser.data_url == 'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1257786&regions=80,64,38,4,115,83,33,68,70,69,30,86,75,40,1,66,48,110,31,22,71,114&spp=0&nm=139760729'
    assert mocked_parser.nm_id == 139760729


def test_parser_raise_error_when_response_not_200(mocked_parser: WBParser, monkeypatch: MonkeyPatch):
    def not_200_response_get(url, params=None, **kwargs) -> Response:
        response = Response()
        response.status_code = 404
        return response
    monkeypatch.setattr('requests.get', not_200_response_get)
    with pytest.raises(exceptions.ResponseStatusError):
        mocked_parser.get_response()


def test_get_data_from_response(mocked_parser: WBParser):
    response = mocked_parser.get_response()
    data = mocked_parser.get_data(response)
    assert type(data) == dict
    assert data.get('state') == 0
    assert data.get('params') == {"curr": "rub", "spp": 0, "version": 1}
    assert data == {"state":0,"params":{"curr":"rub","spp":0,"version":1},"data":{"products":[{"id":139760729,"root":119430798,"kindId":0,"subjectId":515,"subjectParentId":6258,"name":"iPhone 14 Pro Max 1TB (США)","brand":"Apple","brandId":6049,"siteBrandId":16049,"supplierId":887491,"sale":21,"priceU":19999000,"salePriceU":15799200,"logisticsCost":0,"extended":{"basicSale":21,"basicPriceU":15799200},"saleConditions":11,"pics":4,"rating":4,"feedbacks":7,"volume":9,"colors":[{"name":"фиолетовый","id":15631086}],"promotions":[66080,66925,76394,79972,84211,90172,92132,98660,106351,119518,137206,139413,145733],"sizes":[{"name":"","origName":"0","rank":0,"optionId":237114615,"stocks":[{"wh":507,"qty":28,"time1":5,"time2":21}],"time1":5,"time2":21,"wh":507,"sign":"qbpUZPtGC5CoDO96yUDbTgZnh3I="}],"diffPrice": False,"time1":5,"time2":21,"wh":507}]}}


def test_parser_raise_ResponseStatusError_with_bad_data(mocked_parser: WBParser):
    with pytest.raises(exceptions.ParseError):
        mocked_parser.parse_data({'data': 'i am bad data'})


def test_parser_return_WBSchema(mocked_parser: WBParser):
    response = mocked_parser.get_response()
    data = mocked_parser.get_data(response)
    json_schema = mocked_parser.parse_data(data)
    assert isinstance(json_schema, WBSchema)
