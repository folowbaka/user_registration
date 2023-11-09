import pytest

from user_registration.crud import user
from user_registration.schemas.user import UserCreate, UserUpdate


@pytest.mark.parametrize("email, expected", [
    ("notexist@test.com", None),
    ("exist@test.com", "exist@test.com"),
])
def test_get_by_email(postgresql, email, expected):
    res_user = user.get_by_email(postgresql, email)
    assert res_user.email == expected if res_user else res_user == expected


@pytest.mark.parametrize("user_to_create", [
    UserCreate(email="toto@test.com", password="password"),
    UserCreate(email="toto2@test.com", password="password", is_activated=True)
])
def test_create(postgresql, user_to_create):
    res_create = user.create(postgresql, user_to_create)
    assert res_create.email == user_to_create.email
    assert res_create.hashed_password == user_to_create.password
    assert not res_create.is_activated


@pytest.mark.parametrize("user_to_update, expected", [
    (UserUpdate(id=1, email="exist@test.com"), 1),
    (UserUpdate(id=3, email="notexist@test.com"), None),
])
def test_update_is_activated(postgresql, user_to_update, expected):
    res_update = user.update_is_activated(postgresql, user_to_update)
    assert res_update == expected
