from typing import List, Union
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel
from datetime import date, timedelta
from sqlalchemy import or_, extract, and_


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone_number = body.phone_number,
        birth_date = body.birth_date
        )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Union[str, None]:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session)  -> Union[str, None]:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(skip: int, limit: int, query: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(
        or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
    ).offset(skip).limit(limit).all()


async def get_coming_birthday(skip: int, limit: int, db: Session) -> List[Contact]:
    today = date.today()
    end_day = today + timedelta(days=7)

    print()

    return db.query(Contact).filter(
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
    ).offset(skip).limit(limit).all()