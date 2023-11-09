from typing import Generator
from user_registration.db.db_connector import db_connector
from psycopg2 import DatabaseError


def get_con() -> Generator:
    if not db_connector.pool:
        db_connector.pool = db_connector.open_pool()
    db = None
    try:
        db = db_connector.pool.getconn()
        yield db
    except DatabaseError as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if db_connector.pool:
            db_connector.pool.putconn(db)
