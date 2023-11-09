import pytest

from user_registration.crud import user_activation_code
from user_registration.schemas.user_activation_code import UserActivationCodeCreate


@pytest.mark.parametrize("user_activation_code_to_create", [
    UserActivationCodeCreate(code=6666, user_id=1)
])
def test_create(postgresql, user_activation_code_to_create):
    res_create = user_activation_code.create(postgresql, user_activation_code_to_create)
    assert res_create.code == user_activation_code_to_create.code
    assert res_create.user_id == user_activation_code_to_create.user_id


@pytest.mark.parametrize("user_id, code", [
    (1, 6666)
])
def test_get_valid_by_user_id_and_code(postgresql, user_id, code):
    res_get = user_activation_code.get_valid_by_user_id_and_code(postgresql, user_id, code)
    assert not res_get
