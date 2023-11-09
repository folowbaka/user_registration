from fastapi import FastAPI, Depends

from user_registration.core.config import settings
from user_registration.api.api_v1.api import api_router

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)
