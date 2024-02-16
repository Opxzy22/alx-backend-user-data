#!/usr/bin/env python3
"""
    basic authentication Model
"""
from api.v1.auth.auth import Auth
from models.user import User
import re
import base64
from typing import TypeVar
from flask import abort


class BasicAuth(Auth):
    """ basic authentication class
    """
    def extract_base64_authorization_header(self,
            authorization_header: str) -> str:
        """ base64 authorization header

        Args:
            authorization_header (str): the string that start with basic.

        Returns:
            str: the base64 string extracted
        """
        if authorization_header:
            if isinstance(authorization_header, str):
                if authorization_header.startswith('Basic '):
                    return authorization_header[len('Basic '):].strip()
        return None

    def def decode_base64_authorization_header(self,
            base64_authorization_header: str) -> str:
        """ decode base64 authorization header

        Args:
            base64_authorization_header (str): the encoded string

        Returns:
            str: the decoded string
        """
        auth_header = base64_authorization_header
        try:
            if auth_header:
                if isinstance(auth_header, str):
                    decoded_string: bytes = base64.b64decode(auth_header)
                    return auth_header.decode('utf-8')
        except base64.binascii.Error:
            return None

     def user_object_from_credentials(self, user_email: str,
             user_pwd: str) -> TypeVar('User'):
         """
            a method that check if the database have a user
            check if the email and password is valid
            if valid it return the user
        """
         if not user_email or not user_pwd:
             return None
         if type(user_email) != str or type(user_pwd) != str:
             return None
         try:
            database = User.search()
            if len(database) == 0:
                return None
            for user in database:
                if user.email = user_email:
                    if user.is_valid_password(user_pwd):
                        return user
                return None
        except:
            return None
