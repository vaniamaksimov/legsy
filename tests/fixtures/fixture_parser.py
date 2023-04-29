import pytest
from pytest import MonkeyPatch
from requests import Response

from legsy.parser import WBParser


@pytest.fixture
def nm_id() -> int:
    nm_id = 139760729
    return nm_id


@pytest.fixture
def mocked_response() -> Response:
    response = Response()
    response.status_code = 200
    response._content = b'{"state":0,"params":{"curr":"rub","spp":0,"version":1},"data":{"products":[{"id":139760729,"root":119430798,"kindId":0,"subjectId":515,"subjectParentId":6258,"name":"iPhone 14 Pro Max 1TB (\xd0\xa1\xd0\xa8\xd0\x90)","brand":"Apple","brandId":6049,"siteBrandId":16049,"supplierId":887491,"sale":21,"priceU":19999000,"salePriceU":15799200,"logisticsCost":0,"extended":{"basicSale":21,"basicPriceU":15799200},"saleConditions":11,"pics":4,"rating":4,"feedbacks":7,"volume":9,"colors":[{"name":"\xd1\x84\xd0\xb8\xd0\xbe\xd0\xbb\xd0\xb5\xd1\x82\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9","id":15631086}],"promotions":[66080,66925,76394,79972,84211,90172,92132,98660,106351,119518,137206,139413,145733],"sizes":[{"name":"","origName":"0","rank":0,"optionId":237114615,"stocks":[{"wh":507,"qty":28,"time1":5,"time2":21}],"time1":5,"time2":21,"wh":507,"sign":"qbpUZPtGC5CoDO96yUDbTgZnh3I="}],"diffPrice":false,"time1":5,"time2":21,"wh":507}]}}'
    return response


@pytest.fixture
def mocked_parser(nm_id: int, mocked_response: Response, monkeypatch: MonkeyPatch):
    def mocked_get(url, params=None, **kwargs) -> Response:
        return mocked_response
    monkeypatch.setattr('requests.get', mocked_get)
    parser = WBParser(nm_id)
    return parser
