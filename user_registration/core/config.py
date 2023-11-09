import logging
import ecs_logging
import sys


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "user_registration"
    LOGGER_LEVEL: str = "DEBUG"

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    SMTP_TLS: bool
    SMTP_HOST: str
    SMTP_PORT: str
    FAKESMTP_AUTHENTICATION_USERNAME: str
    FAKESMTP_AUTHENTICATION_PASSWORD: str

    EMAIL_TEMPLATES_DIR: str = "/app/user_registration/static/email_templates/build"

    class Config:
        env_file = ".env"


settings = Settings()

logger = logging.getLogger(settings.PROJECT_NAME)
logger.setLevel(settings.LOGGER_LEVEL)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)
