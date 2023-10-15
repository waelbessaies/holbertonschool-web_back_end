#!/usr/bin/env python3
"""
define a _hash_password method
"""
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> str:
    """
    hash  the input password
    """
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """ authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
         return a new user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')
