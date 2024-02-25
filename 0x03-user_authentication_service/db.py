#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str)  -> User:
        """ add a user with email and password
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """a method that query the database
            Kwargs: keyword argument to be queried in the DB
            raise NoResultFound error if no user found
            raise InvalidRequestError if invalid query request
            returns user if found
        """
        if not kwargs:
            raise InvalidRequestError
        valid_attrs = ['id', 'email',
                       'hashed_password',
                       'session_id', 'reset_token']
        for key in kwargs.keys():
            if key not in valid_attrs:
                raise InvalidRequestError
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound
    def update_user(self, user_id: int, **kwargs) -> None:
        """
            a method that update a user
            finds the user by id with the find_user_by method
            loops through the key word arg to be update
            updates and commit
            raise value error if arg does not correspond with
            user attribute
        """
        try:
            user = self.find_user_by(id=user_id)

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            self._session.commit()

        except ValueError:
            raise ValueError('Error')
