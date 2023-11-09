from typing import Any, Optional
from user_registration.schemas.user import UserCreate, UserUpdate
from user_registration.models.user import User


class CRUDUser:

    def get_by_email(self, db: Any, email: str) -> Optional[User]:
        cursor = db.cursor()
        cursor.execute(f"SELECT id, email, password, is_activated FROM users WHERE users.email='{email}'")
        res_get_user = cursor.fetchone()
        if res_get_user:
            res_get_user = User(id=res_get_user[0],
                                email=res_get_user[1],
                                hashed_password=res_get_user[2],
                                is_activated=res_get_user[3])

        return res_get_user

    def create(self, db: Any, obj_in: UserCreate) -> Optional[User]:
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO users (email,password) VALUES('{obj_in.email}', '{obj_in.password}') RETURNING id, password, is_activated")
        inserted_user_id = cursor.fetchone()
        if inserted_user_id:
            db.commit()
            inserted_user = User(id=inserted_user_id[0],
                                 email=obj_in.email,
                                 hashed_password=inserted_user_id[1],
                                 is_activated=inserted_user_id[2])
            return inserted_user

    def update_is_activated(self, db: Any, obj_in: UserUpdate) -> Optional[User]:
        cursor = db.cursor()
        cursor.execute(f"UPDATE users SET is_activated='True' WHERE id={obj_in.id} RETURNING id")
        updated_user_id = cursor.fetchone()
        if updated_user_id:
            db.commit()
            updated_user_id = updated_user_id[0]
        return updated_user_id


user = CRUDUser()
