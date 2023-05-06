import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    update_avatar,
    confirmed_email
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, refresh_token='qwerty123', email='test@test.com', confirmed=False)

    def tearDown(self) -> None:
        self.user = User(id=1, refresh_token='qwerty123', email='test@test.com', confirmed=False)

    async def test_get_user_by_email(self):
        self.session.query().filter().first.return_value = self.user
        result = await get_user_by_email(email='test@test.com', db=self.session)
        self.assertEqual(result, self.user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email='test@test.com', db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(
            username='Testo',
            email='test@test.com',
            password='test1234'
        )
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)

    async def test_update_token(self):
        token = 'test_token123'
        await update_token(user=self.user, token=token, db=self.session)
        self.assertEqual(self.user.refresh_token, token)

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        await confirmed_email(email='test@test.com', db=self.session)
        self.session.commit.return_value = None
        self.assertEqual(self.user.confirmed, True)

    async def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user
        await update_avatar(email='test@test.com', url='test_avatar', db=self.session)
        self.session.commit.return_value = None
        self.assertEqual(self.user.avatar, 'test_avatar')


if __name__ == '__main__':
    unittest.main()
