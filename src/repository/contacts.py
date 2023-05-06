from typing import List
from datetime import datetime, timedelta

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param skip: int: Skip a certain number of records
    :param limit: int: Limit the number of contacts returned
    :param user: User: Get the user id from the user object
    :param db: Session: Access the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact_by_id(contact_id: int, user: User, db: Session) -> Contact:
    """
    The get_contact_by_id function returns a contact from the database by its id.

    :param contact_id: int: Pass the contact id to the function
    :param user: User: Get the user's id, which is used to filter the contacts
    :param db: Session: Pass the database session to the function
    :return: The contact with the given id
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contacts_by_info(information: str, user: User, db: Session) -> List[Contact]:
    """
    The get_contacts_by_info function takes in a string of information, a user object, and the database session.
    It then returns all contacts that match the given information.

    :param information: str: Filter the contacts by firstname, lastname or email
    :param user: User: Get the user id from the database
    :param db: Session: Access the database
    :return: A list of contacts that match the information provided by the user
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == user.id).filter(or_(Contact.firstname == information,
                                                                           Contact.lastname == information,
                                                                           Contact.email == information, )).all()


async def get_contacts_7days_birthdays(user: User, db: Session) -> List[Contact] | None:
    """
    The get_contacts_7days_birthdays function returns a list of contacts whose birthdays are within the next 7 days.
        Args:
            user (User): The User object for which to retrieve contacts.
            db (Session): A database session object used to query the database.

    :param user: User: Get the user id from the user object
    :param db: Session: Pass in the database session
    :return: A list of contacts whose birthday is within the next 7 days
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    current_date = datetime.now()
    end_date = current_date + timedelta(days=7)
    birthdays_7days_list = []
    if contacts:
        for contact in contacts:
            this_year_birthday = contact.birthday.replace(year=current_date.year)
            if current_date < this_year_birthday <= end_date:
                birthdays_7days_list.append(contact)
        return birthdays_7days_list
    else:
        return None


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param user: User: Get the user id from the token
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(
        firstname=body.firstname,
        lastname=body.lastname,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated ContactModel object with new values for firstname, lastname, email, phone and birthday.
            user (User): The User object that is currently logged in and making this request. This is used to ensure that only contacts belonging to this user are updated by themselfs or an admin/superuser.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param body: ContactModel: Pass the contact information to be updated
    :param user: User: Get the user id of the current user
    :param db: Session: Access the database
    :return: The updated contact
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            user (User): The user who owns the contacts list.
            db (Session): A connection to our database, used for querying and deleting data.

    :param contact_id: int: Identify the contact to be removed
    :param user: User: Get the user id from the database
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
