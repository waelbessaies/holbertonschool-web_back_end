#!/usr/bin/env python3
""" 
This module provides authentication functionality.
"""

from typing import Union
from user import User
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ 
    Hash a user's password for storage in the database.
    """
    salted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return salted_password


def _generate_uuid() -> str:
    """ 
    Generate a UUID (Universally Unique Identifier).
    """
    return str(uuid4())


class Auth:
    """ 
    Auth class for managing user authentication and sessions.
    """

    def __init__(self):
        """ 
        Initialize the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ 
        Register a new user with a unique email and password.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            new_registry = self._db.add_user(email, _hash_password(password))
            return new_registry
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ 
        Validate a user's login credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """ 
        Create a user session and return a session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """ 
        Retrieve a user based on their session ID.
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ 
        Destroy a user's session by removing the session ID.
        """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ 
        Generate and return a reset password token for a user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ 
        Update a user's password using a reset token.
        """
        if not reset_token:
            return None
        if not password:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_pwd = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_pwd,
            reset_token=None)
