#!/usr/bin/env python3
""" 
This module provides database functionality for user management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """ 
    DB class for managing the database operations.
    """

    def __init__(self):
        """ 
        Initialize the DB class and create a database.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ 
        Memoized session object for database operations.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_password) -> User:
        """ 
        Add a user to the database with the provided email and hashed password.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ 
        Find a user in the database based on provided criteria.
        """
        try:
            record = self._session.query(User).filter_by(**kwargs).first()
        except TypeError:
            raise InvalidRequestError
        if record is None:
            raise NoResultFound
        return record

    def update_user(self, user_id: int, **kwargs) -> None:
        """ 
        Update user information in the database.
        """
        usr = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(usr, key):
                raise ValueError
            setattr(usr, key, value)
        self._session.commit()
