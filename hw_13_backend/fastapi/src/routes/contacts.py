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
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/search", response_model=List[ContactResponce])
async def search_contacts(skip: int = 0, limit: int = 100, query: str = Query(min_length=1), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts(skip, limit, query, current_user, db)
    return contact


@router.get("/birthdays", response_model=List[ContactResponce])
async def coming_birthdays(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_coming_birthday(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponce)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponce,
description='No more than 10 requests per minute',
dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponce)
async def update_contact(body: ContactModel, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contacts_id}", response_model=ContactResponce)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact