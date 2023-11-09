from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pathlib import Path
from psycopg2.pool import SimpleConnectionPool
from random import randint

from user_registration import dependencies
from user_registration import crud, schemas
from user_registration.utils import send_email
from user_registration.core.security import get_password_hash, verify_password
from user_registration.core.config import settings
from user_registration.models.user_activation_code import UserActivationCode

router = APIRouter()
security = HTTPBasic()


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: SimpleConnectionPool = Depends(dependencies.get_con),
        user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists in our system.",
        )
    user_in.password = get_password_hash(user_in.password)
    user_created = crud.user.create(db, obj_in=user_in)
    return user_created


@router.post("/request-activation-mail/{email}", response_model=str)
def send_activation_mail(
        email: str,
        db: SimpleConnectionPool = Depends(dependencies.get_con),
) -> Any:
    """
    Forward an email that include a 4 digits code to a SMTP server
    """
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email doesn't exists in our system.",
        )
    if user.is_activated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email is already activated",
        )
    email_subject = f"{settings.PROJECT_NAME} - Your account activation code"
    code = randint(0, 9999)
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "activation_email.html") as f:
        template_str = f.read()
    # It's a synchronous process,
    # ideally the mail process should be managed in a asynchronous way with a celery worker or in another dedicated app using a queue
    res = send_email(email, email_subject, template_str,
                     {"project_name": settings.PROJECT_NAME, "activation_code": code})
    if not res:
        raise HTTPException(
            status_code=503,
            detail="The service is unavailable, please retry later on.",
        )
    activation_code = UserActivationCode(code=code, user_id=user.id)
    crud.user_activation_code.create(db, obj_in=activation_code)
    print(activation_code.code)
    return ("Your request has been acknowledged , you 'll receive an email with a code to activate your account."
            "Check your email here http://localhost:8080/")


@router.post("/activate/{code}", response_model=str)
def activate_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        code: int,
        db: SimpleConnectionPool = Depends(dependencies.get_con),
) -> Any:
    """
    Activate the logged user with the provided code if it's correct (under 1 minutes from its creation)
    """
    user = crud.user.get_by_email(db, email=credentials.username)
    is_correct_password = verify_password(credentials.password, user.hashed_password) if user else False
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if user.is_activated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This user is already activated",
        )
    activation_code = crud.user_activation_code.get_valid_by_user_id_and_code(db, user_id=user.id, code=code)
    if not activation_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect code or code has expired",
        )
    if not crud.user.update_is_activated(db, obj_in=user):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="This user can't be activated",
        )

    return "Your account is now activated"
