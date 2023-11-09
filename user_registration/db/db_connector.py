import psycopg2
from psycopg2 import pool
from user_registration.core.config import settings, logger


class DBConnector:
    def __init__(self, db_user, db_password, db_host, db_port, db_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.pool = self.open_pool()

    def __del__(self):
        self.close_pool()

    def open_pool(self):
        psycopg2_pool = None
        try:
            psycopg2_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                               user=self.db_user,
                                                               password=self.db_password,
                                                               host=self.db_host,
                                                               port=self.db_port,
                                                               database=self.db_name)
            if psycopg2_pool:
                logger.info("Database connection established")

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error while connecting to PostgreSQL : {error}")

        finally:
            return psycopg2_pool

    def close_pool(self):
        if self.pool:
            self.pool.closeall()
            logger.info("Database connection closed")


db_connector = DBConnector(db_user=settings.POSTGRES_USER,
                           db_password=settings.POSTGRES_PASSWORD,
                           db_host=settings.POSTGRES_HOST,
                           db_port=settings.POSTGRES_PORT,
                           db_name=settings.POSTGRES_DB)
