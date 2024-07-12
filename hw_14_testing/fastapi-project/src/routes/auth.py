from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.services.email import send_email

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user.

    :param body: User data for registration.
    :type body: UserModel
    :param background_tasks: Object for adding background tasks.
    :type background_tasks: BackgroundTasks
    :param request: FastAPI request object.
    :type request: Request
    :param db: Database session.
    :type db: Session
    :return: If registration is successful, a dictionary containing information about the created user and a success message. If a user with the given email already exists, exception.
    :rtype: dict or HTTPException
    """
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a new user.

    :param body: The OAuth2 password request form containing username and password.
    :type body: OAuth2PasswordRequestForm
    :param db: Database session.
    :type db: Session
    :return: If authentication is successful, a dictionary containing access token, refresh token, and token type. If the email is invalid, not confirmed, or the password is incorrect, exception.
    :rtype: dict or HTTPException
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Confirm user's email using a token.
    :param token: The confirmation token sent to the user's email.
    :type token: str
    :param db: Database session.
    :type db: Session
    :return: A dictionary with a message indicating the result of the email confirmation process. If user confirmed or not exist it returns exception.
    :rtype: dict or HTTPException
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    Request email confirmation for a user.

    :param body: The request body containing the user's email.
    :type body: RequestEmail
    :param background_tasks: Object for adding background tasks.
    :type background_tasks: BackgroundTasks
    :param request: FastAPI request object.
    :type request: Request
    :param db: Database session.
    :type db: Session
    :return: A dictionary with a message indicating the result of the email confirmation request.
    :rtype: dict
    """
    user = await repository_users.get_user_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh the access token using a valid refresh token.
    
    :param credentials: The HTTP Authorization credentials containing the refresh token.
    :type credentials: HTTPAuthorizationCredentials
    :param db: Database session.
    :type db: Session
    :return: A dictionary containing new access token, refresh token, and token type if successful. If the refresh token is invalid, it raises an exception.
    :rtype: dict or HTTPException
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
