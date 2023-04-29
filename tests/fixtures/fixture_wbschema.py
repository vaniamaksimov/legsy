import pytest


good_data = {
  "params": {
    "curr": "rub",
  },
  "data": {
    "products": [
      {
        "id": 139760729,
        "name": "iPhone 14 Pro Max 1TB (США)",
        "brand": "Apple",
        "brandId": 6049,
        "siteBrandId": 16049,
        "supplierId": 887491,
        "sale": 21,
        "priceU": 19999000,
        "salePriceU": 15799200,
        "rating": 4,
        "feedbacks": 7,
        "colors": [
          {
            "name": "фиолетовый",
            "id": 15631086
          }
        ],
        "sizes": [
          {
            "name": "",
            "stocks": [
              {
                "wh": 507,
                "qty": 28,
                "time1": 5,
                "time2": 21
              },
              {
                "wh": 507,
                "qty": 11,
                "time1": 5,
                "time2": 21
              }
            ],
          }
        ],
      }
    ]
  }
}

bad_params = {
  "params": {
    "curr": "i am not a rubble",
  },
  "data": {
    "products": [
      {
        "id": 139760729,
        "name": "iPhone 14 Pro Max 1TB (США)",
        "brand": "Apple",
        "brandId": 6049,
        "siteBrandId": 16049,
        "supplierId": 887491,
        "sale": 21,
        "priceU": 19999000,
        "salePriceU": 15799200,
        "rating": 4,
        "feedbacks": 7,
        "colors": [
          {
            "name": "фиолетовый",
            "id": 15631086
          }
        ],
        "sizes": [
          {
            "name": "",
            "stocks": [
              {
                "wh": 507,
                "qty": 28,
                "time1": 5,
                "time2": 21
              },
              {
                "wh": 507,
                "qty": 11,
                "time1": 5,
                "time2": 21
              }
            ],
          }
        ],
      }
    ]
  }
}


no_sizes = {
  "params": {
    "curr": "rub",
  },
  "data": {
    "products": [
      {
        "id": 139760729,
        "name": "iPhone 14 Pro Max 1TB (США)",
        "brand": "Apple",
        "brandId": 6049,
        "siteBrandId": 16049,
        "supplierId": 887491,
        "sale": 21,
        "priceU": 19999000,
        "salePriceU": 15799200,
        "rating": 4,
        "feedbacks": 7,
        "colors": [
          {
            "name": "фиолетовый",
            "id": 15631086
          }
        ],
        "sizes": [],
      }
    ]
  }
}


no_products = {
  "params": {
    "curr": "rub",
  },
  "data": {
    "products": []
  }
}


@pytest.fixture
def wb_data() -> dict:
    return good_data
