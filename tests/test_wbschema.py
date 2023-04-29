import pytest
from pydantic import ValidationError

from legsy.schemas import WBSchema
from legsy.schemas.WBJson import SizeSchema, WBJsonProductSchema
from tests.fixtures.fixture_wbschema import bad_params, no_products, no_sizes


def test_wbschema_data(wb_data: dict):
    schema = WBSchema(**wb_data)
    params = schema.params
    assert params.curr == 'rub'
    product = schema.data.products[0]
    product: WBJsonProductSchema
    assert product.nm_id == 139760729
    assert product.name == "iPhone 14 Pro Max 1TB (США)"
    assert product.brand == "Apple"
    assert product.brand_id == 6049
    assert product.site_brand_id == 16049
    assert product.supplier_id == 887491
    assert product.sale == 21
    assert product.price == 199_990
    assert product.sale_price == 157_992
    assert product.rating == 4
    assert product.feedbacks == 7
    size = product.sizes[0]
    size: SizeSchema
    assert size.name == 'Без размера'
    assert size.stock == 39
    colors = product.colors[0]
    assert colors.name == 'фиолетовый'


@pytest.mark.parametrize(
        argnames=['test_input', 'expected'],
        argvalues=[
            ((bad_params), (ValidationError)),
            ((no_sizes), (ValidationError)),
            ((no_products), (ValidationError))
        ]
)
def test_wbschema_raise_validation_error(test_input: dict, expected):
    with pytest.raises(expected):
        WBSchema(**test_input)
