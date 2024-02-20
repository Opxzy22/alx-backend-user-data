import bcrypt
from db import DB
from user import User

class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash the input password using bcrypt hashpw

        Args:
            password: Input password string

        Returns:
            bytes: Salted hash of the input password
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    
    def register_user(self, email: str, password: str) -> User:
        """ a method that regiser a new user
        """
        try:
            self._db.find_user_by(email=email)
        except:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)
        
        raise ValueError('User {} already exist'.format(email))
        