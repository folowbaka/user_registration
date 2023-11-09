from typing import Any, Optional
from user_registration.schemas.user_activation_code import UserActivationCodeCreate
from user_registration.models.user_activation_code import UserActivationCode


class CRUDUserActivationCode:

    def create(self, db: Any, obj_in: UserActivationCodeCreate) -> Optional[UserActivationCode]:
        cursor = db.cursor()
        inserted_code = None
        cursor.execute(f"INSERT INTO user_activation_codes (code, user_id, creation_date) "
                       f"VALUES('{obj_in.code}', '{obj_in.user_id}', current_timestamp) "
                       f"ON CONFLICT (user_id) DO UPDATE SET code='{obj_in.code}', creation_date=current_timestamp "
                       f"RETURNING id, creation_date")
        inserted_code_id = cursor.fetchone()
        if inserted_code_id:
            db.commit()
            inserted_code = UserActivationCode(id=inserted_code_id[0],
                                               code=obj_in.code,
                                               user_id=obj_in.user_id,
                                               creation_date=inserted_code_id[1])
        return inserted_code

    def get_valid_by_user_id_and_code(self, db: Any, user_id: str, code: int) -> Optional[UserActivationCode]:
        cursor = db.cursor()
        cursor.execute(f"SELECT id, code, user_id, creation_date FROM user_activation_codes WHERE "
                       f"user_id='{user_id}' AND code='{code}' AND "
                       f"(extract(epoch from current_timestamp - creation_date) / 60)<1")
        res_get_activation_code = cursor.fetchone()
        if res_get_activation_code:
            res_get_activation_code = UserActivationCode(id=res_get_activation_code[0],
                                                         code=res_get_activation_code[1],
                                                         user_id=res_get_activation_code[2],
                                                         creation_date=res_get_activation_code[3])

        return res_get_activation_code


user_activation_code = CRUDUserActivationCode()
