from typing import Union

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> Union[User, None]:
    """
    Retrieves a user from the database by their email address.

    :param email: The email address of the user to find.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The User object if found, or None if no user with the given email exists.
    :rtype: User | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user in the database with optional avatar.

    :param body: The user data model containing user information.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created User object.
    :rtype: User

    This function attempts to fetch a image for the user's email.
    If successful, it sets this as the user's avatar. If unsuccessful,
    it prints the error and proceeds without an avatar.
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: Union[str, None], db: Session) -> None:
    """
    Updates the refresh token for a given user.

    :param user: The user whose token needs to be updated.
    :type user: User
    :param token: The new refresh token. Can be a string or None to remove the token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None
    :rtype: None

    This function updates the refresh_token field of the user and commits the change to the database.
    If token is None, it effectively removes the refresh token for the user.
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Marks the user's email as confirmed in the database.

    :param email: The email address of the user to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the avatar URL for a user identified by their email.

    :param email: The email address of the user whose avatar needs to be updated.
    :type email: str
    :param url: The new avatar URL.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated User object.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


