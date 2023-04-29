from fastapi import FastAPI
import pytest
from fastapi.testclient import TestClient

from legsy.main import app


pytest_plugins = [
    'tests.fixtures.fixture_parser',
    'tests.fixtures.fixture_wbschema',
]


@pytest.fixture
def application():
    return app


@pytest.fixture
def client(application: FastAPI):
    with TestClient(app=application) as client:
        yield client
