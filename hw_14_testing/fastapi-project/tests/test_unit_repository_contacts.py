import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from datetime import date, timedelta

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactRequest, ContactResponce
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    search_contacts,
    get_coming_birthday,
)


class TestContact(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]

        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(first_name="test", last_name="test", email="test@example.com", phone_number="1234567890", birth_date="1990-01-01")
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.birth_date, date(1990, 1, 1))
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(first_name="Updated", last_name="User", email="updated@example.com", phone_number="0987654321", birth_date="1995-05-05")
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, "Updated")
        self.assertEqual(result.email, "updated@example.com")

    async def test_update_contact_not_found(self):
        body = ContactModel(first_name="Updated", last_name="User", email="updated@example.com", phone_number="0987654321", birth_date="1995-05-05")        
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts(self):
        contacts = [Contact(first_name="John"), Contact(last_name="Doe")]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await search_contacts(skip=0, limit=10, query="John", user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_coming_birthday(self):
        today = date.today()
        upcoming_birthday = today + timedelta(days=5)
        contact_with_birthday = Contact(first_name="Birthday", birth_date=upcoming_birthday)
        self.session.query().filter().offset().limit().all.return_value = [contact_with_birthday]
        result = await get_coming_birthday(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, [contact_with_birthday])


if __name__ == '__main__':
    unittest.main()