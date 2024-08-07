from typing import List, Union
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel
from datetime import date, timedelta
from sqlalchemy import or_, extract, and_


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Retrieves a list of contacts for a specific user with specified pagination parameters.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: Contact
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :type body: ContactModel
    :param user: The user to create the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created contact.
    :rtype: Contact
    """
    contact = Contact(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone_number = body.phone_number,
        birth_date = body.birth_date,
        user_id = user.id
        )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Union[str, None]:
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactModel
    :param user: The user to update the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated contact, or None if it does not exist.
    :rtype: str | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session)  -> Union[str, None]:
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The user to remove the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed contact, or None if it does not exist.
    :rtype: str | None
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(skip: int, limit: int, query: str, user: User, db: Session) -> Union[List[Contact], None]:
    """
    Searches for contacts for a specific user based on a query string.

    :param skip: The number of notes to skip.
    :type skip: int
    :param limit: The maximum number of notes to return.
    :type limit: int
    :param query: The search query string. Contacts are searchable by first name, last name, or email address.
    :type query: str
    :param user: The user to retrieve the contacts for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of matching contacts, or None if it does not exist.
    :rtype: List[Contact] | None
    """
    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
    ).offset(skip).limit(limit).all()


async def get_coming_birthday(skip: int, limit: int, user: User, db: Session) -> Union[List[Contact], None]:
    """
    Retrieves contacts with birthdays coming up in the next 7 days for a specific user.

    :param skip: The number of contacts to skip.
    :type skip: int
    :param limit: The maximum number of contacts to return.
    :type limit: int
    :param user: The user to retrieve the contact for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of contacts with upcoming birthdays, or None if no contacts found.
    :rtype: List[Contact] | None
    """
    today = date.today()
    end_day = today + timedelta(days=7)

    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            or_(
                and_(
                    extract('month', Contact.birth_date) == extract('month', today),
                    extract('day', Contact.birth_date) >= extract('day', today),
                ),
                and_(
                    extract('month', Contact.birth_date) == extract('month', end_day),
                    extract('day', Contact.birth_date) < extract('day', end_day)
                ),
            )
        )
    ).offset(skip).limit(limit).all()