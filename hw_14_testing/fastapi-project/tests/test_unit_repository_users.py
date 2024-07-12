import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel

# Import the functions you want to test
from src.repository.users import (
    get_user_by_email, 
    create_user, 
    update_token, 
    confirmed_email, 
    update_avatar
)


class TestUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email="test@example.com", username="testuser")
        self.user_data = UserModel(email="new@example.com", username="newuser", password="password")

    async def test_create_user(self):
        result = await create_user(self.user_data, self.session)

        self.assertEqual(result.email, "new@example.com")
        self.assertEqual(result.username, "newuser")
        self.assertIsNotNone(result.avatar)

    async def test_get_user_by_email(self):
        self.session.query().filter().first.return_value = self.user

        result = await get_user_by_email(email=self.user.email, db=self.session)

        self.assertIsNotNone(result)
        self.assertEqual(result.email, self.user.email)

    async def test_update_token(self):
        self.session.query().filter().first.return_value = self.user
        token = "new_token"

        await update_token(self.user, token, self.session)

        self.assertEqual(self.user.refresh_token, token)

    async def test_update_token_none(self):
        await update_token(self.user, None, self.session)

        self.assertIsNone(self.user.refresh_token)

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user

        await confirmed_email(self.user.email, self.session)

        updated_user = await get_user_by_email(self.user.email, self.session)
        self.assertTrue(updated_user.confirmed)

    async def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user
        new_avatar_url = "http://example.com/new_avatar.jpg"

        result = await update_avatar(self.user.email, new_avatar_url, self.session)

        self.assertEqual(result.avatar, new_avatar_url)


if __name__ == '__main__':
    unittest.main()