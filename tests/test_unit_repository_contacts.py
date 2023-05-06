from datetime import datetime, timedelta
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contact_by_id,
    get_contacts,
    get_contacts_7days_birthdays,
    get_contacts_by_info,
    create_contact,
    remove_contact,
    update_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found_id(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result_id = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result_id, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact_by_id(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_get_contacts_found_information(self):
        contacts = [Contact(firstname='Test', lastname='Tests', email='test@test.com')]
        self.session.query().filter().filter().all.return_value = contacts

        result_info_firstname = await get_contacts_by_info(information='Test', user=self.user, db=self.session)
        self.assertEqual(result_info_firstname, contacts)

        result_info_lastname = await get_contacts_by_info(information='Tests', user=self.user, db=self.session)
        self.assertEqual(result_info_lastname, contacts)

        result_info_email = await get_contacts_by_info(information='test@test.com', user=self.user, db=self.session)
        self.assertEqual(result_info_email, contacts)

    async def test_get_contacts_information_not_found(self):
        self.session.query().filter().filter().all.return_value = None

        result_info_firstname = await get_contacts_by_info(information='Test', user=self.user, db=self.session)
        self.assertIsNone(result_info_firstname)

        result_info_lastname = await get_contacts_by_info(information='Tests', user=self.user, db=self.session)
        self.assertIsNone(result_info_lastname)

        result_info_email = await get_contacts_by_info(information='test@test.com', user=self.user, db=self.session)
        self.assertIsNone(result_info_email)

    async def test_get_contacts_7days_birthdays_found(self):
        contacts = [Contact(birthday=datetime.now()+timedelta(days=1))]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts_7days_birthdays(user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_7days_birthdays_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_contacts_7days_birthdays(user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(
            firstname='Test',
            lastname='Tests',
            email='test@test.com',
            phone='0998887766',
            birthday=datetime.now()-timedelta(weeks=250),
            user_id=self.user.id
        )
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
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
        body = ContactModel(
            firstname='Test',
            lastname='Tests',
            email='test@test.com',
            phone='0998887766',
            birthday=datetime.now() - timedelta(weeks=250),
            user_id=self.user.id
        )
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(
            firstname='Test',
            lastname='Tests',
            email='test@test.com',
            phone='0998887766',
            birthday=datetime.now() - timedelta(weeks=250),
            user_id=self.user.id
        )
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
