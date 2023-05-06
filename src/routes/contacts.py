from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_contacts(skip: int = 0, limit: int = 25, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip a number of records
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Get the database session
    :param current_user: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_contact_id(contact_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contact_id function is a GET request that returns the contact with the given ID.
    If no such contact exists, it raises an HTTP 404 error.

    :param contact_id: int: Specify the contact id that is passed in the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/{information}", response_model=List[ContactResponse],
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_contacts_info(information: str, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts_info function will return a contact based on the information provided.
        The function takes in an information parameter, which is used to search for a contact.
        If no contacts are found, then the function returns an HTTP 404 error.

    :param information: str: Get the information from the url
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contacts_by_info(information, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/get/7-birthdays", response_model=List[ContactResponse], description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def read_contacts_7days_birthdays(db: Session = Depends(get_db),
                                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_contacts_7days_birthdays function returns a list of contacts that have birthdays in the next 7 days.
        The function takes two parameters: db and current_user.
        The db parameter is used to access the database, while current_user is used to get information about the user who made this request.

    :param db: Session: Get the database connection
    :param current_user: User: Get the current user's id and pass it to the function
    :return: A list of contacts that have birthdays in the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts_7days_birthdays(current_user, db)
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Validate the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user that is logged in
    :return: A contactmodel object
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactModel object containing the new values for the contact.
            - contact_id: An integer representing the ID of an existing contact to be updated.
            - db (optional): A Session object used to connect to and query a database, if not provided, one will be created automatically using get_db().

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Identify the contact to be deleted
    :param db: Session: Get a database session
    :param current_user: User: Get the user that is currently logged in
    :return: A contactmodel object, but the function is not annotated with a return type
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 10 requests per minute',
               dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user from the database
    :return: The contact that was removed
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
