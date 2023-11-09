from typing import Dict, Generator

import pytest
import psycopg2

from fastapi.testclient import TestClient
from pytest_postgresql import factories
from unittest.mock import Mock
from user_registration import dependencies

from asgi import app

postgresql = factories.postgresql(
        "postgresql_noproc",
        load=["/app/sql/create_tables.sql",
              "/app/user_registration/tests/sql/user_fixture.sql",
              "/app/user_registration/tests/sql/user_activation_code_fixture.sql"])


@pytest.fixture()
def db(postgresql):
    app.dependency_overrides[dependencies.get_con] = lambda: postgresql


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

