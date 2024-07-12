from typing import List, Union
from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.schemas import ContactModel, ContactResponce
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.services.auth import Auth
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])

auth_service = Auth()


@router.get("/", response_model=List[ContactResponce],
description='No more than 10 requests per minute',
dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of contacts for the current user.

    :param skip: Number of contacts to skip.
    :type skip: int
    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param db: Database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: List of contacts.
    :rtype: List[ContactResponce]
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/search", response_model=List[ContactResponce])
async def search_contacts(skip: int = 0, limit: int = 100, query: str = Query(min_length=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Search contacts for the current user.

    :param skip: Number of contacts to skip.
    :type skip: int
    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param query: Search query string.
    :type query: str
    :param db: Database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: List of matching contacts.
    :rtype: List[ContactResponce]
    """
    contact = await repository_contacts.search_contacts(skip, limit, query, current_user, db)
    return contact


@router.get("/birthdays", response_model=List[ContactResponce])
async def coming_birthdays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve contacts with upcoming birthdays for the current user.

    :param skip: Number of contacts to skip.
    :type skip: int
    :param limit: Maximum number of contacts to return.
    :type limit: int
    :param db: Database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: List of contacts with upcoming birthdays.
    :rtype: List[ContactResponce]
    """
    contacts = await repository_contacts.get_coming_birthday(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponce)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieve a specific contact by ID for the current user.

    :param contact_id: ID of the contact to retrieve.
    :type contact_id: int
    :param db: Database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The requested contact if found else exception.
    :rtype: ContactResponce or HTTPException
    """
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponce,
description='No more than 10 requests per minute',
dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Create a new contact for the current user.

    :param body: Contact details.
    :type body: ContactModel
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: Session
    :return: The created contact.
    :rtype: ContactResponce
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponce)
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Update an existing contact for the current user.

    :param body: Updated contact details.
    :type body: ContactModel
    :param contact_id: ID of the contact to update.
    :type contact_id: int
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: Session
    :return: The updated contact if found else exception.
    :rtype: ContactResponce or HTTPException
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contacts_id}", response_model=ContactResponce)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    Remove a contact for the current user.

    :param contact_id: ID of the contact to remove.
    :type contact_id: int
    :param current_user: The current authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: Session
    :return: The removed contact if found else exception.
    :rtype: ContactResponce or HTTPException
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact