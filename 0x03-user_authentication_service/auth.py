import bcrypt
from db import DB
from user import User
import uuid

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
                if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                    return True
                return False
        except:
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
        except:
            return None

