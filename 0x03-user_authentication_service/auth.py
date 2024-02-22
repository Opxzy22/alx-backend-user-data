import bcrypt
from db import DB
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    hash a password using bcrypt

    Args:
        password (str): password to hash
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
        generate a new uuid and return it as a string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ a method that regiser a new user
        """
        try:
            self._db.find_user_by(email=email)
        except ValueError:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

        raise ValueError('User {} already exist'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        valid user credentials for authorization

        Args:
            email (str): user email
            password (str): user password

        Returns:
            bool: true or false
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                if bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password):
                    return True
                return False
        except ValueError:
            return False

    def create_session(self, email: str) -> str:
        """ find a user by email
            generate a uuid with the _generate_uuid function
            update the user session_id with the generaed uuid
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except ValueError:
            return None

    def get_user_from_session_id(self, session_id) -> Union[User, None]:
        """
        get the user from the provided session id

        Args:
            session_id (str): string

        Returns:
            User: current user object
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy a user session_id
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user is not None:
                user.session_id = None
                self._db.update_user(user_id, user.session_id)
                return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ find user by email
        generate uuid and set it as the reset_token in db
        """
        try:
            user = self._db.find_user_by(email)
            if user:
                reset_token = _generate_uuid()
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except ValueError:
            raise ValueError

    def reset_password(self, reset_token: str, password: str) -> None:
        """ find user with reset token
            hash the new password and update it in db
        """
        try:
            user = self._db.find_user_by(reset_token)
            if user:
                hashed_password = _hash_password(password)
                self._db.update_user(reset_token=None,
                                     hashed_password=hashed_password)
        except ValueError:
            raise ValueError
