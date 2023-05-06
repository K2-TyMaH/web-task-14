from sqlalchemy import Column, Integer, String, func, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy_utils import PhoneNumberType

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint('phone', 'user_id', name='unique_phone_user'),)

    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), index=True, nullable=False)
    lastname = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    birthday = Column(DateTime, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
