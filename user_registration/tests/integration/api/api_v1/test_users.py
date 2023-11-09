import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from fastapi import status
from requests.auth import HTTPBasicAuth

from user_registration.core.config import settings


@pytest.mark.parametrize("email, expected", [
    ("notexist@test.com", status.HTTP_200_OK),
    ("exist@test.com", status.HTTP_400_BAD_REQUEST),
])
def test_create_user(
        client: TestClient, db, email, expected
) -> None:
    data = {"email": email, "password": "password"}
    r = client.post(f"{settings.API_V1_STR}/users/", json=data)
    assert r.status_code == expected
    user_created = r.json()
    if "detail" in user_created:
        assert user_created["detail"] == "A user with this email already exists in our system."
    else:
        assert user_created["email"] == email
        assert user_created["id"]


@pytest.mark.parametrize("email, send_mail,expected", [
    ("notexist@test.com", None, status.HTTP_404_NOT_FOUND),
    ("activated@test.com", None, status.HTTP_400_BAD_REQUEST),
    ("exist@test.com", None, status.HTTP_503_SERVICE_UNAVAILABLE),
    ("exist@test.com", True, status.HTTP_200_OK)
])
def test_send_activation_mail(
        client: TestClient, db, monkeypatch, email, send_mail, expected
) -> None:
    monkeypatch.setattr("user_registration.api.api_v1.endpoints.users.send_email", Mock(return_value=send_mail))
    r = client.post(f"{settings.API_V1_STR}/users/request-activation-mail/{email}")
    assert r.status_code == expected


@pytest.mark.parametrize("email, expected", [
    ("notexist@test.com", status.HTTP_200_OK),
])
def test_create_and_activate_user(
        client: TestClient, db, monkeypatch, email, expected
) -> None:
    data = {"email": email, "password": "password"}
    r = client.post(f"{settings.API_V1_STR}/users/", json=data)
    user_created = r.json()
    code = 6666
    monkeypatch.setattr("user_registration.api.api_v1.endpoints.users.send_email", Mock(return_value=True))
    monkeypatch.setattr("user_registration.api.api_v1.endpoints.users.randint", Mock(return_value=code))
    client.post(f"{settings.API_V1_STR}/users/request-activation-mail/{user_created['email']}")
    r = client.post(f"{settings.API_V1_STR}/users/activate/{code}",
                    auth=HTTPBasicAuth(user_created["email"],data["password"])
    )
    assert r.status_code == expected
    assert r.json() == "Your account is now activated"

